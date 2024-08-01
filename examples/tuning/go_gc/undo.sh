#!/bin/sh
# Copyright (c) 2020 Huawei Technologies Co., Ltd.
# A-Tune is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR
# PURPOSE.
# See the Mulan PSL v2 for more details.
# Create: 2020-10-30

path=$(
  cd "$(dirname "$0")"
  pwd
)

echo "undo the client and server yaml files"
sed -i "s#sh $path/go_gc.sh#sh .*/go_gc.sh#g" $path/go_gc_client.yaml
sed -i "s#cat $path/go_gc.sh#cat .*/go_gc.sh#g" $path/go_gc_server.yaml
sed -i "s#' $path/go_gc.sh#' .*/go_gc.sh#g" $path/go_gc_server.yaml

echo "restore the server yaml file to /etc/atuned/tuning/"
rm /etc/atuned/tuning/go_gc_server.yaml
cp $path/go_gc_server.yaml /etc/atuned/tuning/
