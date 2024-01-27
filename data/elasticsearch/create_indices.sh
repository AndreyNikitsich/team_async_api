#!/bin/sh

es_url="http://localhost:9200"

indexes=$(ls /data_builder/indexes/*.json)

for eachfile in $indexes
do
  index_name=$(basename -- "$eachfile" | cut -d '.' -f1)
  echo "Create index $index_name from $eachfile"
  request_url="$es_url/$index_name"
  cat "$eachfile" | curl -XPUT "$request_url" -H 'Content-Type: application/json' -d @-
done
