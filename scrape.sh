#!/bin/bash

i=0
while [ $i -lt 38748 ]
do
    echo >&2 $i
    wget -O html_doc "http://myanimelist.net/users.php?q=&show="$i --quiet
    i=$(( $i + 25 ))
    python scrape.py
done