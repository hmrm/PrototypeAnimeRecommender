#!/bin/bash

for i in {1..8}
do
    echo "Factor "$i
    echo ""
    echo "Positive"
    for i in {1..10}
    do 
	read -r line
	curl "http://mal-api.com/anime/"$line | ruby getname.rb
    done
    echo ""
    echo "Negative"
    for i in {1..10}
    do 
	read -r line
	curl "http://mal-api.com/anime/"$line | ruby getname.rb
    done
    echo ""
    echo ""
done