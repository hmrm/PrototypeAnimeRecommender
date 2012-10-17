#!/bin/bash

i=0
while [ $i -lt 972600 ]
do
    echo >&2 "Scraping 25 starting from "$i
    curl "http://myanimelist.net/users.php?q=&show="$i | python scrape.py
    i=$(( $i + 25 ))
    echo >&2 ""
done