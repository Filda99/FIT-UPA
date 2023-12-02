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
    processor_value = ""
    internal_storage_value = ""
    ram_value = ""
    gpu_value = ""
    
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
    numeric_price = re.sub(r'\D', '', price_text.split(',')[0])
    numeric_price = int(numeric_price)

    # ---------------------
    # Get specs
    proc_done = ram_done = stor_done = gpu_done = False
    
    for item in soup.find_all('div', class_='one-list-item'):
        subtitle = item.find('div', class_='one-list-item__subtitle').text.strip()
        title = item.find('div', class_='one-list-item__title').text.strip()

        # Check for specific subtitles and store corresponding values
        if "Prozessor" in subtitle:
            processor_value = title
            proc_done = True
        elif "Arbeitsspeicher" in subtitle:
            ram_value = title
            ram_done = True
        elif "SSD" in subtitle:
            internal_storage_value = title
            stor_done = True
        elif "Grafikkarte" in subtitle:
            gpu_value = title
            gpu_done = True

    if not proc_done:
        processor_value = "Unknown"
    if not ram_done:
        ram_value = "0"
    if not stor_done:
        internal_storage_value = "0"
    if not gpu_done:
        gpu_value = "Unknown"
        
    print (link, name, price, processor_value, internal_storage_value, ram_value, gpu_value)
    
    
def get_names_and_prices_from_link_list(links):
    # delay in seconds
    delay = 1
    
    data = []
    t = tqdm(links)
    t.set_description("Number of pages proceed: ")
    for l in t:
        link = l.strip()
        get_name_and_price_from_link(link)
        
        # there is a request limit preventing DDOS attacks on the page so we have to wait some time
        sleep(delay)   
    
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
    

def main():
    # parsing arguments which must be in format
    # python3 parse_urls.py <count_to_parse> <file_with_urls> <file_to_store>
    # examples:
    #   python3 parse_urls.py
    #   python3 parse_urls.py 20
    #   python3 parse_urls.py 20 urls.txt
    
    count_to_parse = None
    file_with_urls = 'urls.txt'
    
    if len(sys.argv) > 1:
        count_to_parse = int(sys.argv[1])
        if len(sys.argv) > 2:
            file_with_urls = sys.argv[2]

    links = get_links(file_with_urls, count_to_parse)
    get_names_and_prices_from_link_list(links)
    

# if __name__ == "__main__":
main()
