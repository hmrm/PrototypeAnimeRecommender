#!/bin/bash

bash scrape.sh | tee usernames.txt | sed '/^$/d' | bash parse.sh | python reformat.py | tee data.txt | python model.py 10 > results.txt