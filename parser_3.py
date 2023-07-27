import requests
from bs4 import BeautifulSoup
import os
import random
import time
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

cookies = {
    'PHPSESSID': '2k7mfsksi1402rheksl2qlqcq0',
    'JAVASCRIPT': '1',
    '_ga': 'GA1.2.1749448558.1690347979',
    '_gid': 'GA1.2.1295565242.1690347979',
    '_fbp': 'fb.1.1690347978800.541607340',
    '_gat': '1',
    '_ga_W07YKRLB5N': 'GS1.2.1690377558.2.1.1690379387.60.0.0',
}

headers = {
    'authority': 'www.logolounge.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cookie': 'PHPSESSID=2k7mfsksi1402rheksl2qlqcq0; JAVASCRIPT=1; _ga=GA1.2.1749448558.1690347979; _gid=GA1.2.1295565242.1690347979; _fbp=fb.1.1690347978800.541607340; _gat=1; _ga_W07YKRLB5N=GS1.2.1690377558.2.1.1690379387.60.0.0',
    'referer': 'https://www.logolounge.com/logos/winners',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

def get_links():
    logo_hrefs = []
    with open("logolounge_links.txt", "w") as f:
        for i in range(1,4131):
            print(f'crawling page {i} ...')
            url_to_scrape = 'https://www.logolounge.com/logos?page='+str(i)
            response = requests.get(url_to_scrape, cookies=cookies, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            logo_items = soup.find_all('article', class_='logo-item')
            for logo in logo_items:
                href = logo.find('a', class_='logo-item-figure-content')['href']
                f.write('https://www.logolounge.com/' + href + '\n')

    print('done')
    
def save_img(url, fileName):
    response = requests.get(url, stream=True, cookies=cookies, headers=headers)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content))

    if img.mode == "CMYK":
        img = img.convert("RGB")

    if not os.path.exists('./logos3'):
        os.makedirs('logos3')

    img.thumbnail((512, 512))
    img.save(f'./logos3/{fileName}', "PNG")
    



def process_link(link):
    link = link.replace("\n", "")
    dd_client = ''  # Initialize dd_client as an empty string

    try:
        response = requests.get(link, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
                
        #get name and tags
        try:
            dt_client = soup.find('dt', text='Client')
            dd_client = dt_client.find_next('dd').text
            dt_industry = soup.find('dt', text='Industry')
                    
            dd_industry = dt_industry.find_next('dd').text
            fileName = '_'.join([dd_client, dd_industry]).replace('/', ' ')
                    
            dd_tags = dt_industry.find_next('dd').find_next('dd').text.replace('\n','')
            fileName = '_'.join([dd_client, dd_industry, dd_tags]).replace('/', ' ')
            fileName = fileName + '.png'
        except:
            fileName = dd_client + '.png'
                    
        #get logo img and save it
        figure = soup.find('figure', class_='single-logo-figure')
        img_url = figure.find('img')['src']
                
        #save img
        print(f'saving img of {link}...')
        save_img(img_url, fileName)
            
    except Exception as e:
        print(f'something went wrong with {link}')
        print(f"An error occurred: {e}")
        with open("logolounge_scrap_failure.txt", "a") as f:
            f.write(link + '\n')


def scrap():
    file = "logolounge_links.txt"
    start_count = 65099
    count = 0
    
    with open(file, 'r') as f:
        links = f.readlines()
       
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust max_workers as needed
        for link in links:
            if count >= start_count:
                executor.submit(process_link, link)
            count += 1

scrap()