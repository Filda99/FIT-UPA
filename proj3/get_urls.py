import re
import sys
import requests
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup as bs

# https://scrapeops.io/web-scraping-playbook/403-forbidden-error-web-scraping/
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
}

# set num_of_urls from the command line argument
if len(sys.argv) > 1:
    try:
        num_of_urls = int(sys.argv[1])
    except ValueError:
        print("Invalid argument for num_of_urls. Using default value 100.")
        num_of_urls = 100

main_url = 'https://www.one.de'
categories_urls = []
urls_to_process = []
items_urls = []

page = requests.get(main_url, headers=HEADERS)
soup = bs(page.content, 'html.parser')

####################################################################################

# 1) find categories on the main page
def get_category_urls(main_url):
    page = requests.get(main_url, headers=HEADERS)
    soup = bs(page.content, 'html.parser')

    # find categories in soup
    categories_ul = soup.find('ul', class_='navigation--list categories')

    if categories_ul:
        # iterate through <li> elements to extract category URLs
        for li in categories_ul.find_all('li'):
            category_url = li.find('a')['href']
            categories_urls.append(category_url)

# 2) find specified number of product urls (category is not important)
def get_urls(url_to_analyze, num_of_urls):
    page = requests.get(url_to_analyze, headers=HEADERS)
    soup = bs(page.content, 'html.parser')
    num_of_obtained_products = 0

    t = tqdm(total=num_of_urls)
    t.set_description("Number of urls")

    # obtain number of pages
    paging_display = soup.find('span', class_='paging--display')
    if paging_display:
        num_pages_match = re.search(r'von (\d+)', paging_display.text)
        if num_pages_match:
            num_pages = int(num_pages_match.group(1))

            # loop through each page & get products urls
            for page_num in range(1, num_pages + 1):
                page_url = f"{url_to_analyze}?p={page_num}"

                 # get product URLs on the current page
                 # only iterate for a needed amount of urls, else break
                if num_of_obtained_products < num_of_urls:
                    num_of_obtained_products += extract_product_urls(page_url)
                    t.update(num_of_obtained_products)
                else:
                    t.close()
                    break

def extract_product_urls(page_url):
    page = requests.get(page_url, headers=HEADERS)
    soup = bs(page.content, 'html.parser')
    num_of_items_on_page = 0

    sleep(1)   

    # Extract href attribute from each product item
    product_links = soup.find_all('a', class_='product__link')
    for product_link in product_links:
        items_urls.append(product_link['href'])
        num_of_items_on_page += 1
    
    return num_of_items_on_page

####################################################################################

# get all categories
get_category_urls(main_url)
# choose category
url_to_analyze = categories_urls[1] # https://www.one.de/pc-systeme/one-gaming-pcs/

# get products urls
get_urls(url_to_analyze, num_of_urls)

# now the urls are saved in items_urls
items_urls = items_urls[:num_of_urls] # only save the needed amount of urls

# print output
for url in items_urls:
    print(url)