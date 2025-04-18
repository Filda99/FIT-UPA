import sys
import requests
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup as bs
import re

# https://scrapeops.io/web-scraping-playbook/403-forbidden-error-web-scraping/
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}

def get_name_and_price_from_link(link):
    name = ""
    price = ""
    processor_name = ""
    storage = ""
    ram = ""
    gpu = ""
    
    page = requests.get(link, headers=HEADERS)
    soup = bs(page.content, 'html.parser')
    main_content = soup.find('div', class_='product--detail-upper block-group')
    
    # content found
    if main_content is None:
        print (link, "Unknown", "Unknown", "Unknown", "Unknown", "Unknown", "Unknown")
        return 

    # ---------------------
    # Get name
    name = main_content.find('h1', class_='product--title').text.strip()
    
    # ---------------------
    # Get price
    price_span = main_content.find('span', class_='price--content')
    # Extract the text inside the span
    price_text = price_span.text.strip()
    # Extract only the numeric part of the price
    try:
        price = re.match(r'[\d\.\,]+\s€', price_text).group(0)
    except:
        price = "Unknown price"

    # ---------------------
    # Get specs
    proc_done = ram_done = stor_done = gpu_done = False
    
    for item in soup.find_all('div', class_='one-list-item'):
        subtitle = item.find('div', class_='one-list-item__subtitle').text.strip()
        title = item.find('div', class_='one-list-item__title').text.strip()

        # Check for specific subtitles and store corresponding values
        if "Prozessor" in subtitle:
            processor_name = title
            proc_done = True
        elif "Arbeitsspeicher" in subtitle:
            ram = title
            ram_done = True
        elif "SSD" in subtitle:
            storage = title
            stor_done = True
        elif "Grafikkarte" in subtitle:
            gpu = title
            gpu_done = True

    if not proc_done:
        processor_name = "Unknown"
    if not ram_done:
        ram = "0"
    if not stor_done:
        storage = "0"
    if not gpu_done:
        gpu = "Unknown"
        
    print(link, name, price, processor_name, storage, ram, gpu, sep="\t")
    
def get_names_and_prices_from_link_list(links):
    data = []
    t = tqdm(links)
    t.set_description("Number of pages processed: ")
    for l in t:
        link = l.strip()
        get_name_and_price_from_link(link)
        
        # there is a request limit preventing DDOS attacks on the page so we have to wait some time
        sleep(1)   
    
    return data

def get_links(file_name, count):
    lines = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    
    if count is not None:
        if len(lines) < count:
            print("ERROR: not enough urls in file, processing", len(lines), "urls.")
        elif len(lines) > count:
            lines = lines[:count]

    return lines

####################################################################################

def main():
    # parsing arguments which must be in format
    # python3 parse_urls.py <count_to_parse> <file_with_urls>
    # examples:
    #   python3 parse_urls.py
    #   python3 parse_urls.py 20
    #   python3 parse_urls.py 20 urls.txt
    
    count_to_parse = 1
    file_with_urls = 'urls.txt'
    
    if len(sys.argv) > 1:
        count_to_parse = int(sys.argv[1])
        if len(sys.argv) > 2:
            file_with_urls = sys.argv[2]

    links = get_links(file_with_urls, count_to_parse)
    get_names_and_prices_from_link_list(links)
    
if __name__ == "__main__":
    main()
