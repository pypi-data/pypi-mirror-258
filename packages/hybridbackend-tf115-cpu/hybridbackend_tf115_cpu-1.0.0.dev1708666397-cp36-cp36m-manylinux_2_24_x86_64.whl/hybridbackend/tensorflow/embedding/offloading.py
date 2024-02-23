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

r'''Offloaded embedding lookup related classes and functions.
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import functools

from tensorflow.python.framework import ops
from tensorflow.python.ops import state_ops
from tensorflow.python.ops import variables

from hybridbackend.tensorflow.embedding.service import EmbeddingService


class EmbeddingServiceForVariable(EmbeddingService):
  r'''A Caching for Variable.
  '''
  def pull(self, storage, keys):
    r'''Pull embeddings from storage.
    '''
    return self._lookup_fn_(storage, keys)

  def push(self, storage, keys, values):
    r'''Push values to storage.
    '''
    return state_ops.scatter_update(storage, keys, values)


class EmbeddingOffloading(object):  # pylint: disable=useless-object-inheritance
  r'''Offloading embedding params to remote storage.
  '''
  @classmethod
  def build_params(cls, cache_capacity=32, get_var_offloading=None):
    r'''Decorator to build params.
    '''
    def fn_wrapper(fn):
      @functools.wraps(fn)
      def wrapped_fn(*args, collections=None, **kwargs):
        if cache_capacity < 1:
          return fn(*args, collections=collections, **kwargs)
        offloaded = EmbeddingServiceForVariable(
          cache_capacity, get_var_offloading, fn, *args,
          collections=collections, **kwargs)
        ops.add_to_collection(EmbeddingOffloading.__name__, offloaded)
        return offloaded.params
      return wrapped_fn
    return fn_wrapper

  @classmethod
  def lookup(cls, fn):
    r'''Decorator to lookup embeddings.
    '''
    def lookup_fn_wrapper(fn, *args, **kwargs):
      @functools.wraps(fn)
      def wrapped_lookup_fn(params, ids):
        return fn(params, ids, *args, **kwargs)
      return wrapped_lookup_fn

    @functools.wraps(fn)
    def wrapped_fn(params, ids, *args, **kwargs):
      if isinstance(params, list):
        target_param = params[0]
      else:
        target_param = params
      if isinstance(target_param, variables.Variable):
        params_name = target_param.name.split(':')[0]
      else:
        params_name = target_param.name.split('/read:')[0]

      items = ops.get_collection_ref(EmbeddingOffloading.__name__)
      found = None
      for item in items:
        if item.name == params_name:
          found = item
          break
      if found is None:
        return fn(params, ids, *args, **kwargs)
      return found.lookup(
        lookup_fn_wrapper(fn, *args, **kwargs), ids)
    return wrapped_fn
