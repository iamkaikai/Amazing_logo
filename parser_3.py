import requests
from bs4 import BeautifulSoup
import os
import random
import time
from PIL import Image
import io
from concurrent.futures import ThreadPoolExecutor

cookies = {
    'JAVASCRIPT': '1',
    '_ga': 'GA1.2.355474566.1688918118',
    '_fbp': 'fb.1.1688918119209.1138937444',
    'PHPSESSID': 'k79dsj31ihpn32r70062ugud86',
    '_gid': 'GA1.2.1917758118.1690514693',
    '_gat': '1',
    '_ga_W07YKRLB5N': 'GS1.2.1690514693.7.1.1690514701.52.0.0',
}

headers = {
    'authority': 'www.logolounge.com',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'JAVASCRIPT=1; _ga=GA1.2.355474566.1688918118; _fbp=fb.1.1688918119209.1138937444; PHPSESSID=k79dsj31ihpn32r70062ugud86; _gid=GA1.2.1917758118.1690514693; _gat=1; _ga_W07YKRLB5N=GS1.2.1690514693.7.1.1690514701.52.0.0',
    'referer': 'https://www.logolounge.com/logos',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-origin',
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
        start_time = time.time()
        response = requests.get(link, cookies=cookies, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        response_time= round(response_time, 2)
        soup = BeautifulSoup(response.text, 'html.parser')
                
        #get name and tags
        try:
            dt_client = soup.find('dt', string='Client')
            if not dt_client:
                print('check point a')
                dd_client = soup.find('h1', class_='vcard-heading').text.replace('\n','')
            else:
                print('check point a2')
                dd_client = dt_client.find_next('dd').text
                
            fileName = dd_client
            
            print('check point b')
            dt_industry = soup.find('dt', string='Industry')        
            dd_industry = dt_industry.find_next('dd').text
            fileName = '_'.join([dd_client, dd_industry]).replace('/', ' ')
                    
            print('check point c')
            dd_tags = dt_industry.find_next('dd').find_next('dd').text.replace('\n','')
            dd_tags = ' '.join(set(dd_tags.split()))
            
            print('check point d')
            fileName = '_'.join([dd_client, dd_industry, dd_tags]).replace('/', ' ').replace(' .png', '.png')
            fileName = fileName + '.png'
            words_to_replace = ['design', 'logo', 'image', 'icon', 'Icon']
            for word in words_to_replace:
                fileName = fileName.replace(word, '')
        except:
            fileName = dd_client + '.png'
                    
        #get logo img and save it
        figure = soup.find('figure', class_='single-logo-figure')
        img_url = figure.find('img')['src']
                
        #save img
        print('--------------------- ✅')
        print(f'saving img of {link}...')
        print(f'client = {dd_client}')
        print(f'file name = {fileName}')
        print('Response time: {} seconds'.format(response_time))
        print('---------------------\n')
        save_img(img_url, fileName)
            
    except Exception as e:
        print('--------------------- ❌')
        print(f'something went wrong with {link}')
        print(f"An error occurred: {e}")
        print('---------------------\n')
        with open("logolounge_scrap_failure.txt", "a") as f:
            f.write(link + '\n')


def scrap():
    file = "logolounge_links.txt"
    start_count = 203669
    count = 0
    
    with open(file, 'r') as f:
        links = f.readlines()
       
    with ThreadPoolExecutor(max_workers=8) as executor:  # Adjust max_workers as needed
        for link in links:
            if count >= start_count:
                executor.submit(process_link, link)
                time.sleep(random.randint(1, 5))
            count += 1

scrap()