#! /bin/bash

python3 get_urls.py 100 > urls_test.txt
python3 parse_urls.py 10 urls_test.txt

