#! /bin/bash

source superlativ_upa_proj3/bin/activate # Actiave preinstalled venv from build.sh

python3 get_urls.py 100 > urls_test.txt 2>/dev/null
python3 parse_urls.py 10 urls_test.txt 2>/dev/null

