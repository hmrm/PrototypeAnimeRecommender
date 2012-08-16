#!/bin/bash

i=1

while read -r line
do
    echo $i $line >&2
    i=$(( $i + 1))
    curl "http://mal-api.com/animelist/"$line | ruby parse_json.rb
done