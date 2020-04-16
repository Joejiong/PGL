# Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved
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
"""
Utils for the models.
"""
import paddle.fluid as fluid
from paddle.fluid.layer_helper import LayerHelper


def lookup_table(input, embedding_table, dtype='float32'):
    """
    lookup table support for paddle.
    :param input:
    :param embedding_table:
    :param dtype:
    :return:
    """
    is_sparse = False
    is_distributed = False
    helper = LayerHelper('embedding', **locals())
    remote_prefetch = is_sparse and (not is_distributed)
    if remote_prefetch:
        assert is_sparse is True and is_distributed is False
    tmp = helper.create_variable_for_type_inference(dtype)
    padding_idx = -1
    helper.append_op(
        type='lookup_table',
        inputs={'Ids': input,
                'W': embedding_table},
        outputs={'Out': tmp},
        attrs={
            'is_sparse': is_sparse,
            'is_distributed': is_distributed,
            'remote_prefetch': remote_prefetch,
            'padding_idx': padding_idx
        })
    return tmp


def lookup_table_gather(index, input):
    """
    lookup table support for paddle by gather.
    :param index:
    :param input:
    :return:
    """
    return fluid.layers.gather(index=index, input=input, overwrite=False)
