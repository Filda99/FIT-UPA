#! /bin/bash

python3 get_urls.py 100 > urls.txt
python3 parse_urls.py 100 urls.txt > data.tsv

