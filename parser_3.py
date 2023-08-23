import requests
from bs4 import BeautifulSoup
import os
import random
import time
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
import csv

load_dotenv()

proxy_list = []
proxy_user = os.getenv('proxy_user')
proxy_password = os.getenv('proxy_password')
proxy_key = os.getenv('proxy_key')
Image.MAX_IMAGE_PIXELS = 300000000 
print(proxy_user)
print(proxy_password)
print(proxy_key)

with open('proxies.txt', 'r') as f:
    proxies = f.read().split('\n')
    for proxy in proxies:
        proxy_list.append({
            'http': f"http://{proxy_user}:{proxy_password}@{proxy}",
            'https': f"http://{proxy_user}:{proxy_password}@{proxy}",
        }
    )

# print(proxy_list)
    
cookies = {
    '_ga': 'GA1.2.1749448558.1690347979',
    '_fbp': 'fb.1.1690347978800.541607340',
    'PHPSESSID': '2ggm338vbnfj5j9p9vgngslo46',
    '_gid': 'GA1.2.1842192523.1692760340',
    'JAVASCRIPT': '1',
    '_gat': '1',
    '_ga_W07YKRLB5N': 'GS1.2.1692795656.11.1.1692796959.60.0.0',
}

headers = {
    'authority': 'www.logolounge.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': '_ga=GA1.2.1749448558.1690347979; _fbp=fb.1.1690347978800.541607340; PHPSESSID=2ggm338vbnfj5j9p9vgngslo46; _gid=GA1.2.1842192523.1692760340; JAVASCRIPT=1; _gat=1; _ga_W07YKRLB5N=GS1.2.1692795656.11.1.1692796959.60.0.0',
    'referer': 'https://www.logolounge.com/logos/452066',
    'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
}



def get_links(page):
    links = []
    print(f'crawling page {page} ...')
    url_to_scrape = 'https://www.logolounge.com/logos?page='+str(page)
    response = requests.get(url_to_scrape, cookies=cookies, headers=headers)
    print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    logo_items = soup.find_all('article', class_='logo-item')
    
    for logo in logo_items:
        href = logo.find('a', class_='logo-item-figure-content')['href']
        
        print(href)
        links.append('https://www.logolounge.com/' + href)

    links = sorted(list(set(links)))

    with open("logolounge_links.txt", "w") as f:
        for link in links:
            f.write(link + '\n')
            
    print('done')
    
def save_img(url, fileName, proxy):
    response = requests.get(url, stream=True, cookies=cookies, headers=headers, proxies=proxy)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content))

    if img.mode == "CMYK":
        img = img.convert("RGB")

    img.info.pop('icc_profile', None)
    
    if not os.path.exists('./logos3'):
        os.makedirs('logos3')

    img.thumbnail((1024, 1024))
    
    fileName = fileName.replace('/','')
    img.save(f'./logos3/{fileName}.png', "PNG")
    
def extract_detail(dt_label, soup):
    dt_element = soup.find('dt', string=dt_label)
    
    if dt_label == 'Art Director' and not dt_element:
        dt_element = soup.find('dt', string='Creative Director')

    if dt_element and dt_element.find_next('dd'):
        return dt_element.find_next('dd').text
    return None

def process_link(link, proxy, count):
    link = link.replace("\n", "")
    csv_file = 'l3-metadata.csv'
    
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['file_name', 'page_url', 'logo_url', 'title', 'designer', 'creative director', 'client', 'industry', 'tags', 'description'])
    else:
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)      
            try:
                start_time = time.time()
                response = requests.get(link, cookies=cookies, headers=headers, proxies=proxy)
                response.encoding = 'utf-8'
                end_time = time.time()
                response_time= round(end_time - start_time, 2)
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # title
                title = soup.find('h1', class_='vcard-heading').text.replace('\n','')    
                    
                # client, designer, creative_director, industry
                client = extract_detail('Client', soup)
                designer = extract_detail('Designer', soup)
                creative_director = extract_detail('Art Director', soup)
                industry = extract_detail('Industry', soup)
                
                # tags
                tags_elements = soup.find_all('a', class_='tag')
                tags = [tag.text for tag in tags_elements]
                tags = None if not tags else tags
                                    
                #get logo img and save it
                figure = soup.find('figure', class_='single-logo-figure')
                img_url = figure.find('img')['src']
                
                #description
                parent_div = soup.find('div', class_='single-logo-item')
                description = parent_div.find('p').text.replace('\n', '').replace(',', ' ') if parent_div and parent_div.find('p') else None

                
                # file name
                fileName = 'l3-' + str(count)
                writer.writerow([fileName, link, img_url, title, designer, creative_director, client, industry, tags, description])

                #save img
                print('--------------------- ✅')
                print(f'count = {count}...')
                print(f'saving img of {link}...')
                print(f'file name = {fileName}.png')
                print(f'title = {title}')
                print(f'designer = {designer}')
                print(f'creative director = {creative_director}')
                print(f'client = {client}')
                print(f'industry = {industry}')
                print(f'tags = {tags}')
                print(f'img url = {img_url}')
                print('Response time: {} seconds'.format(response_time))
                print('---------------------\n')
                save_img(img_url, fileName, proxy)
                    
            except Exception as e:
                print('--------------------- ❌')
                print(f'something went wrong with {link}')
                print(f"An error occurred: {e}")
                print('---------------------\n')
                with open("logolounge_scrap_failure.txt", "a") as f:
                    f.write(link + '\n')


def scrap_imgs():
    file = "logolounge_links.txt"
    start_count = 189
    count = 0
    with open(file, 'r') as f:
        links = f.readlines()
    
    with ThreadPoolExecutor(max_workers=40) as executor:
        for link in links:
            # test mode
            # if count > 2:
            #     break
            # print(f'iteration {count}')
            if count >= start_count:
                executor.submit(process_link, link, random.choice(proxy_list), count)
                time.sleep(random.random()+0.2)
            count += 1

def scrap_links():
    for i in range(1,4132):
        get_links(i)
            
# scrap_links()
scrap_imgs()