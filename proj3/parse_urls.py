import sys
import requests
import unicodedata
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup as bs
 
# https://scrapeops.io/web-scraping-playbook/403-forbidden-error-web-scraping/
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}


# https://stackoverflow.com/a/517974
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nfkd_form.encode('ASCII', 'ignore').decode('ASCII')
    return only_ascii


def get_name_and_price_from_link(link):
    
    # debug = False
    debug = True

    if debug:
        print('-------------------')
        print('parsing url:', link)
        
    name = ""
    price = ""
    processor_value = ""
    internal_storage_value = ""
    ram_value = ""
    battery_value = ""
    
    page = requests.get(link, headers=HEADERS)
    soup = bs(page.content, 'html.parser')
    main_content = soup.find('div', class_='product_section js-product_section container is-justify-center')
    
    # content found
    if main_content is not None:
        name = main_content.find('h1', class_='product_name title small-down--hidden').text.strip()
        price = main_content.find('div', class_='price-ui').text.strip()
        
        # Extract Processor
        # .parent.parent is used to get to the row of a table
        processor_row = soup.find('span', class_='spec_header_first', string='Processor').parent.parent
        processor_value = processor_row.find('span', class_='spec_content_first').text.strip()

        # Extract Internal Storage
        internal_storage_row = soup.find('span', class_='spec_header_first', string='Internal Storage').parent.parent
        internal_storage_value = internal_storage_row.find('span', class_='spec_content_first').text.strip()

        # Extract RAM
        ram_row = soup.find('span', class_='spec_header_second', string='RAM').parent.parent
        ram_value = ram_row.find('span', class_='spec_content_second').text.strip()

        # Extract Battery
        battery_row = soup.find('span', class_='spec_header_first', string='Battery').parent.parent
        battery_value = battery_row.find('span', class_='spec_content_first').text.strip()
    else:
        # product not avaliable 
        name = 'Unknown'
        price = "0"
        processor_value = "Unknown"
        internal_storage_value = "0"
        ram_value = "0"
        battery_value = "0"
            
    name = remove_accents(name)
    price = remove_accents(price)
    processor_value = remove_accents(processor_value)
    internal_storage_value = remove_accents(internal_storage_value)
    ram_value = remove_accents(ram_value)
    battery_value = remove_accents(battery_value)
            
    if debug:
        print(name, price, processor_value, internal_storage_value, 
              ram_value, battery_value, '   (', link, ')')
        
    return(name, price, processor_value, internal_storage_value, 
              ram_value, battery_value)
    
    
def get_names_and_prices_from_link_list(links):
    # delay in seconds
    delay = 5
    
    data = []
    for l in tqdm(links):
        link = l.strip()
        name, price, processor_value, internal_storage_value, ram_value, battery_value = get_name_and_price_from_link(link)
        data.append((link, name, price, processor_value, internal_storage_value, ram_value, battery_value))
        
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
    

def store_to_file(file_name, data):
    with open(file_name, "w") as f:
        for link, name, price, processor_value, internal_storage_value, ram_value, battery_value in data:
            f.write(f'{link}\t{name}\t{price}\t{processor_value}\t{internal_storage_value}\t{ram_value}\t{battery_value}\n')


def main():
    # parsing arguments which must be in format
    # python3 parse_urls.py <count_to_parse> <file_with_urls> <file_to_store>
    # examples:
    #   python3 parse_urls.py
    #   python3 parse_urls.py 20
    #   python3 parse_urls.py 20 urls.txt
    #   python3 parse_urls.py 20 urls.txt data.tsv
    
    count_to_parse = None
    file_with_urls = 'urls.txt'
    file_to_store  = 'data.tsv'
    
    if len(sys.argv) > 1:
        count_to_parse = int(sys.argv[1])
        if len(sys.argv) > 2:
            file_with_urls = sys.argv[2]
            if len(sys.argv) > 3:
                file_to_store = sys.argv[3]

    links = get_links(file_with_urls, count_to_parse)
    data = get_names_and_prices_from_link_list(links)
    store_to_file(file_to_store, data)
    

# if __name__ == "__main__":
main()
