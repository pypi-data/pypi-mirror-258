# Copyright 2021 Alibaba Group Holding Limited. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

r'''Embedding service on offloaded storage.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import abc
from collections import namedtuple

from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import tensor_spec
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import custom_gradient
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn_ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import variable_scope as vs
from tensorflow.python.training import training_util

from hybridbackend.tensorflow.distribute.collective import Collective
from hybridbackend.tensorflow.distribute.ops import Topology
from hybridbackend.tensorflow.distribute.partition.ops import \
  partition_by_dual_modulo_stage_one
from hybridbackend.tensorflow.distribute.partition.ops import \
  partition_by_dual_modulo_stage_two
from hybridbackend.tensorflow.distribute.partition.ops import \
  partition_by_modulo
from hybridbackend.tensorflow.framework.context import Context
from hybridbackend.tensorflow.framework.ops import GraphKeys
from hybridbackend.tensorflow.framework.view import OperationLike


class EmbeddingService(
    namedtuple(
      'EmbeddingService', [
        'name', 'params',
        'cache_slab_size', 'cache_size',
        'cache_keys', 'cache_values',
        'cache_steps', 'cache_updates', 'optimizer_states',
        'save_ckpt_update_ops', 'do_eviction'])):
  r'''Embedding service on offloaded storage.
  '''
  class CacheUpdates(object):  # pylint: disable=useless-object-inheritance
    r'''Updates to embedding table cache.
    '''
    def __init__(self):
      self._removed_cache_keys = []
      self._removed_cache_indices = []
      self._added_cache_keys = []
      self._added_cache_indices = []

    def remove(self, key, cache_indices):
      self._removed_cache_keys.append(key)
      self._removed_cache_indices.append(cache_indices)

    def add(self, key, cache_indices):
      self._added_cache_keys.append(key)
      self._added_cache_indices.append(cache_indices)

    def all_removed_cache_indices(self):
      return array_ops.concat(self._removed_cache_indices, axis=0)

    def all_removed_cache_keys(self):
      return array_ops.concat(self._removed_cache_keys, axis=0)

    def all_added_cache_indices(self):
      return array_ops.concat(self._added_cache_indices, axis=0)

    def all_added_cache_keys(self):
      return array_ops.concat(self._added_cache_keys, axis=0)

    def clean_all(self):
      self._removed_cache_keys.clear()
      self._removed_cache_indices.clear()
      self._added_cache_keys.clear()
      self._added_cache_indices.clear()

  EMPTY = - 2 ** 63

  def __new__(
      cls, capacity, get_var_offloading, builder,
      *args, collections=None, **kwargs):
    params_collections = [
      ops.GraphKeys.GLOBAL_VARIABLES,
      GraphKeys.NOT_REPLICATED]
    if collections is not None:
      params_collections = list(set(collections + params_collections))
    params = builder(*args, collections=params_collections, **kwargs)
    name = params.name.split(':')[0]
    cache_slab_size = 32
    try:
      import pycuda.autoinit  # pylint: disable=import-outside-toplevel
      cache_slab_size = pycuda.autoinit.device.get_attribute(
        pycuda.driver.device_attribute.WARP_SIZE)
    except:  # pylint: disable=bare-except
      pass

    prev_get_variable = vs.VariableScope.get_variable
    vs.VariableScope.get_variable = get_var_offloading
    capacity = (capacity // cache_slab_size) * cache_slab_size
    cache_size = vs.get_variable(
      f'{name}_cache_size',
      shape=[],
      dtype=dtypes.int32,
      collections=[ops.GraphKeys.LOCAL_VARIABLES, GraphKeys.NOT_REPLICATED],
      initializer=init_ops.constant_initializer(capacity),
      trainable=False,
      use_resource=True)
    with ops.device('/gpu:0'):
      cache_keys = vs.get_variable(
        f'{name}_cache_keys',
        shape=[capacity],
        dtype=dtypes.int64,
        collections=[ops.GraphKeys.LOCAL_VARIABLES, GraphKeys.NOT_REPLICATED],
        initializer=init_ops.constant_initializer(EmbeddingService.EMPTY),
        trainable=False,
        use_resource=True)
      cache_values = vs.get_variable(
        f'{name}_cache_values',
        shape=[capacity, params.shape[-1]],
        dtype=params.dtype,
        collections=[ops.GraphKeys.LOCAL_VARIABLES, GraphKeys.NOT_REPLICATED],
        initializer=init_ops.zeros_initializer(),
        trainable=True,
        use_resource=True)
    cache_steps = vs.get_variable(
      f'{name}_cache_steps',
      shape=[capacity],
      dtype=dtypes.int64,
      collections=[ops.GraphKeys.LOCAL_VARIABLES, GraphKeys.NOT_REPLICATED],
      initializer=init_ops.constant_initializer(EmbeddingService.EMPTY),
      trainable=False,
      use_resource=True)
    do_eviction = vs.get_variable(
      f'{name}_do_eviction',
      shape=[],
      dtype=dtypes.bool,
      collections=[ops.GraphKeys.LOCAL_VARIABLES, GraphKeys.NOT_REPLICATED],
      initializer=init_ops.constant_initializer(False),
      trainable=False,
      use_resource=True)

    vs.VariableScope.get_variable = prev_get_variable
    cache_updates = cls.CacheUpdates()
    optimizer_states = []
    save_ckpt_update_ops = []
    return super(EmbeddingService, cls).__new__(
      cls, name, params,
      cache_slab_size, cache_size,
      cache_keys, cache_values, cache_steps, cache_updates, optimizer_states,
      save_ckpt_update_ops, do_eviction)

  @abc.abstractmethod
  def pull(self, storage, keys):
    r'''Pull embeddings from storage.
    '''

  @abc.abstractmethod
  def push(self, storage, keys, values):
    r'''Push values to storage.
    '''

  def issharded(self, weights):
    r'''Check whether the embedding weights are sharded.
    '''
    sharded_variables = ops.get_default_graph().get_collection_ref(
      GraphKeys.SHARDED_VARIABLES)
    if weights in sharded_variables:
      return True
    if isinstance(weights, (list, tuple)) and len(weights) == 1:
      weights = weights[0]
      if isinstance(weights, ops.Tensor):
        vname = weights.name.split('/read')[0]
        for v in sharded_variables:
          if vname == v.name.split(':')[0]:
            return True
    return False

  def lookup(self, fn, ids):
    r'''Lookup embeddings from parameters via caching.
    '''
    @custom_gradient.custom_gradient
    def _lookup_op(cache, keys):
      if keys.dtype != dtypes.int64:
        keys = math_ops.cast(keys, dtypes.int64)
      hit_input_indices, hit_cache_indices, miss_input_indices, miss_keys = (
        OperationLike('Lookup')
        .returns_tensors(
          tensor_spec.TensorSpec([None], dtypes.int32),
          tensor_spec.TensorSpec([None], dtypes.int64),
          tensor_spec.TensorSpec([None], dtypes.int32),
          tensor_spec.TensorSpec([None], dtypes.int64))
        .finalize(self.cache_keys, keys, cache_slab_size=self.cache_slab_size))
      hit_values = array_ops.gather(cache, hit_cache_indices)
      keys_shape = array_ops.shape(keys)
      values_last_dim = array_ops.expand_dims(
        array_ops.shape(self.cache_values)[-1], -1)
      values_shape = array_ops.concat([keys_shape, values_last_dim], -1)
      values = array_ops.zeros(
        values_shape, self.params.dtype)
      values = array_ops.tensor_scatter_update(
        values, array_ops.expand_dims(hit_input_indices, -1), hit_values)
      miss_values = self.pull(self.params, miss_keys)
      values = array_ops.tensor_scatter_update(
        values, array_ops.expand_dims(miss_input_indices, -1), miss_values)

      def grad_fn(*grads, **kwargs):
        r'''Gradient function for embedding lookup.
        '''
        num_misses = array_ops.size(miss_keys)
        variables = kwargs.pop('variables', None)
        if variables is None:
          raise ValueError('None variables is fed into grad_fn')

        def _evict():
          step = training_util.get_or_create_global_step()
          num_removes = num_misses - self.cache_size
          hit_steps_updated = state_ops.scatter_update(
            self.cache_steps, hit_cache_indices, -step)
          with ops.control_dependencies([hit_steps_updated]):
            _, removed_cache_indices = nn_ops.top_k(
              self.cache_steps, num_removes, sorted=False)
          steps_removed = state_ops.scatter_update(
            self.cache_steps, removed_cache_indices, EmbeddingService.EMPTY)
          removed_keys = array_ops.gather(
            self.cache_keys, removed_cache_indices)
          self.cache_updates.remove(removed_keys, removed_cache_indices)
          with ops.control_dependencies([removed_keys]):
            keys_removed = state_ops.scatter_update(
              self.cache_keys, removed_cache_indices, EmbeddingService.EMPTY)
          removed_cache_values = array_ops.gather(
            cache, removed_cache_indices)
          params_updated = self.push(
            self.params, removed_keys,
            removed_cache_values)
          with ops.control_dependencies(
              [steps_removed, keys_removed, params_updated]):
            return self.cache_size.assign(0)

        def _inact():
          return self.cache_size.assign_sub(num_misses)

        # TODO: Pack and linearize removal ops
        with ops.control_dependencies([values]):
          self.do_eviction.assign(num_misses > self.cache_size)
          remove_ready = control_flow_ops.cond(
            self.do_eviction, _evict, _inact)
        with ops.control_dependencies([remove_ready]):
          available_cache_indices = array_ops.where(
            math_ops.equal(self.cache_keys, EmbeddingService.EMPTY))
          miss_cache_indices = array_ops.slice(
            array_ops.reshape(available_cache_indices, [-1]),
            array_ops.expand_dims(
              ops.convert_to_tensor(0, dtype=num_misses.dtype), -1),
            array_ops.expand_dims(num_misses, -1))
          reserve_ready = []
          reserve_ready.append(state_ops.scatter_update(
            self.cache_values, miss_cache_indices, miss_values))
          reserve_ready.append(state_ops.scatter_update(
            self.cache_keys, miss_cache_indices, miss_keys))
        self.cache_updates.add(miss_keys, miss_cache_indices)
        cache_indices = array_ops.zeros(array_ops.shape(keys), dtypes.int64)
        cache_indices = array_ops.tensor_scatter_update(
          cache_indices, array_ops.expand_dims(
            hit_input_indices, -1), hit_cache_indices)
        cache_indices = array_ops.tensor_scatter_update(
          cache_indices, array_ops.expand_dims(
            miss_input_indices, -1), miss_cache_indices)
        with ops.colocate_with(cache):
          cache_shape = array_ops.shape(cache)
        with ops.control_dependencies(reserve_ready):
          d_cache = ops.IndexedSlices(
            array_ops.identity(grads[0]), cache_indices, cache_shape)
        return (None, None), [None, d_cache]
      return values, grad_fn

    self._lookup_fn_ = fn
    self.cache_updates.clean_all()
    if not self.issharded(self.params):
      with Context.scope(sharding=False):
        return _lookup_op(self.cache_values, ids)

    local_world_size = Context.get().local_world_size
    num_shards = Context.get().world_size
    num_nodes = Context.get().world_size // local_world_size
    current_device = control_flow_ops.no_op().device

    if (Context.get().options.use_hierarchical_embedding_lookup
        and local_world_size > 1
        and num_nodes > 1):
      with Context.scope(sharding=False):
        with ops.device(Context.get().devices[Context.get().rank]):
          s0_ids_shards, s0_ids_sizes, s0_shard_index =\
            partition_by_dual_modulo_stage_one(
              array_ops.reshape(ids, shape=[-1]),
              local_world_size, num_nodes,
              name='s0_shard_partition')
          s0_shard_ids, s0_shard_sizes = Collective.get().alltoall(
            s0_ids_shards,
            sizes=s0_ids_sizes,
            topology=Topology.INTRA_NODE)

          s0_shard_ids, s0_shard_unique_index = array_ops.unique(
            array_ops.reshape(s0_shard_ids, shape=[-1]),
            name='s0_shard_unique')
          s1_ids_shards, s1_ids_sizes, s1_shard_index =\
            partition_by_dual_modulo_stage_two(
              s0_shard_ids, num_nodes, local_world_size,
              name='s1_shard_partition')
          s1_shard_ids, s1_shard_sizes = Collective.get().alltoall(
            s1_ids_shards,
            sizes=s1_ids_sizes,
            topology=Topology.INTER_NODE)
          s1_shard_ids, s1_shard_unique_index = array_ops.unique(
            array_ops.reshape(s1_shard_ids, shape=[-1]),
            name='s1_shard_unique')

          if self.params not in ops.get_collection_ref(
              GraphKeys.DYNAMIC_VARIABLES):
            s1_shard_ids = s1_shard_ids // Context.get().world_size

          with ops.device(current_device):
            embeddings = _lookup_op(self.cache_values, s1_shard_ids)
            dimension = int(embeddings.shape[-1])

          embeddings = array_ops.gather(
            embeddings, s1_shard_unique_index,
            name='s1_shard_unique_restore')

          embeddings, _ = Collective.get().alltoall(
            embeddings,
            sizes=s1_shard_sizes,
            common_shape=[dimension],
            topology=Topology.INTER_NODE)
          embeddings = array_ops.gather(
            embeddings, s1_shard_index,
            name='s1_shard_stitch')
          embeddings = array_ops.gather(
            embeddings, s0_shard_unique_index,
            name='s0_shard_unique_restore')

          embeddings, _ = Collective.get().alltoall(
            embeddings,
            sizes=s0_shard_sizes,
            common_shape=[dimension],
            topology=Topology.INTRA_NODE)
          embeddings = array_ops.gather(
            embeddings, s0_shard_index,
            name='s0_shard_stitch')
          return embeddings
    else:
      with Context.scope(sharding=False):
        with ops.device(Context.get().devices[Context.get().rank]):
          ids_shards, ids_sizes, shard_index = partition_by_modulo(
            ids, num_shards, name='shard_partition')
          shard_ids, shard_sizes = Collective.get().alltoall(
            ids_shards, sizes=ids_sizes)
          shard_ids, shard_unique_index = array_ops.unique(
            shard_ids, name='shard_unique')
          if self.params not in ops.get_collection_ref(
              GraphKeys.DYNAMIC_VARIABLES):
            shard_ids = shard_ids // num_shards
          with ops.device(current_device):
            embeddings = _lookup_op(self.cache_values, shard_ids)
            dimension = int(embeddings.shape[-1])
          embeddings = array_ops.gather(
            embeddings, shard_unique_index,
            name='shard_unique_restore')
          embeddings, _ = Collective.get().alltoall(
            embeddings,
            sizes=shard_sizes,
            common_shape=[dimension])
          embeddings = array_ops.gather(
            embeddings, shard_index,
            name='shard_stitch')
          return embeddings

  def before_apply_gradients(self, optimizer):
    r'''Update optimizer states before apply.
    '''
    update_ops = []
    self.optimizer_states.clear()

    def _evict(states, states_cache):
      states_to_remove = array_ops.gather(
        states_cache,
        self.cache_updates.all_removed_cache_indices())
      states_removed = self.push(
        states,
        self.cache_updates.all_removed_cache_keys(),
        states_to_remove)
      return states_removed

    def _inact(states):
      return array_ops.identity(states)

    def _remove_ready(states, states_cache):
      remove_ready = control_flow_ops.cond(
        self.do_eviction,
        lambda: _evict(states, states_cache),
        lambda: _inact(states))
      return remove_ready

    for state_name in optimizer.get_slot_names():
      states = optimizer.get_slot(self.params, state_name)
      states_cache = optimizer.get_slot(self.cache_values, state_name)
      self.optimizer_states.append((states, states_cache))

      with ops.control_dependencies([_remove_ready(states, states_cache)]):
        states_to_add = self.pull(
          states,
          self.cache_updates.all_added_cache_keys())
      states_added = state_ops.scatter_update(
        states_cache,
        self.cache_updates.all_added_cache_indices(),
        states_to_add)
      update_ops.append(states_added)
    return control_flow_ops.group(update_ops)

  def before_save_checkpoints(self):
    r'''Update parameters and optimizer states before checkpointing.
    '''
    all_cache_indices = array_ops.where(
      math_ops.not_equal(self.cache_keys, EmbeddingService.EMPTY))
    all_cache_keys = array_ops.gather(self.cache_keys, all_cache_indices)
    all_cache_values = array_ops.gather(self.cache_values, all_cache_indices)
    self.save_ckpt_update_ops.clear()
    self.save_ckpt_update_ops.append(self.push(
      self.params, all_cache_keys, all_cache_values))
    for states, cache_states in self.optimizer_states:
      all_cache_states = array_ops.gather(cache_states, all_cache_indices)
      self.save_ckpt_update_ops.append(
        self.push(states, all_cache_keys, all_cache_states))
