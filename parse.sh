#!/bin/bash

while read -r line
do
    echo $line >&2
    curl "http://mal-api.com/animelist/"$line | ruby parse_json.rb
done