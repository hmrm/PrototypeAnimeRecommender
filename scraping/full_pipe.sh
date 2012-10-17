#!/bin/bash

bash scrape.sh | tee usernames.txt | sed '/^$/d' | bash parse.sh | tee data.txt | python reformat.py | python model.py 10 > results.txt