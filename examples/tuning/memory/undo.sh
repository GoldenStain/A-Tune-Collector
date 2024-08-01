#!/bin/sh

cur=$(
  cd "$(dirname "$0")"
  pwd
)

echo "undo the test script、client and server yaml files"

sed -i "s#cd $cur/#cd stream#g" $cur/tuning_stream_client.yaml
sed -i "s# $cur/Makefile#.stream/Makefile#g" $cur/tuning_stream_server.yaml


echo "restore the server yaml file to /etc/atuned/tuning/"
rm /etc/atuned/tuning/tuning_stream_server.yaml
cp tuning_stream_server.yaml /etc/atuned/tuning/

