#this scrapper is to get all the logos from Logobook.com

import re
import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures


#get all the links of logos
def scrap_link():

    file = "logobook.html"
    logo_hrefs = []

    with open(file, 'r') as f:
        content = f.read()

    pattern_link = r'(http://www\.logobook\.com/(letter/[a-z]/|number-logos/all/|shape/[0-9a-z]*/|object/[0-9a-z\-]*|nature/[0-9a-z\-]*|business/[0-9a-z\-]*))'
    pattern_logo = r"http://www\.logobook\.com/logo/"    
    matches = set(re.findall(pattern_link, content))    #regex links from categories
    
    for link in matches:
            print(f'scraping {link}...')
            base_url = link[0]
            response = requests.get(base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            page_links = soup.findAll(['a'], {'class': 'page-numbers'})
            page_len = len(page_links)
        
            #save starting page
            for a_tag in soup.find_all('a'):
                href = a_tag.get('href')
                if href and re.match(pattern_logo, href):
                    logo_hrefs.append(href)
            
            #save more pages if any(more than 2 pages)
            if page_len > 0:
                pages = [tag['href'] for tag in page_links]
                for p in pages:
                    response = requests.get(p)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.text, 'html.parser')
                
                    for a_tag in soup.find_all('a'):
                        href = a_tag.get('href')
                        if href and re.match(pattern_logo, href):
                            logo_hrefs.append(href)

    with open("links.txt", "w") as f:
        logo_hrefs = set(logo_hrefs)
        for logo_href in logo_hrefs:
            f.write(logo_href + '\n')
            
    print("Link scrapping done...")

def download_logo(link):
    
    response = requests.get(link)
    response.encoding = 'utf-8'
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    file_name = None
    
    #extract logo
    img_link = soup.select('.single-logo .logo-svg img')
    svg = img_link[0]
    company = svg['alt'].replace(' ', '-')
    
    #extract info and tags
    details = soup.select('.single-logo-details')[0]
    tags_html = soup.select('.single-tags')[0]
    h3 = details.findAll('h3')
    
    if h3:
        country = h3[0].find('a').text.replace(' ', '-')
        business = h3[1].find('a').text.replace(' ', '-')
    else:
        country = 'N/A'
        business = 'N/A'

    file_name = f'{company}_{country}_{business}_'    
    file_name = re.sub(r'[\\/:"*?<>|]', '', file_name)  # Remove invalid characters
    
    count = 0
    for tag in tags_html.find_all('a'):
        if count == 0:
            file_name = file_name + tag.text                
        else:
            file_name = file_name + '-' + tag.text
        count +=1
    
    svg_url = svg['src']
    svg_response = requests.get(svg_url)
    svg_response.raise_for_status()
    
    
    with open(f'logos/{file_name}.svg', 'wb') as f:
        f.write(svg_response.content)
        print(f'----------------------------\ndownloading {file_name}...')
    
    with open('downloaded.txt', 'a') as f2:
        f2.write(link + '\n')

if __name__ == '__main__':
    if not os.path.exists('links.txt'):
        print('Start scrapping links...')
        scrap_link()
    else:
        print('links already downloaded.\nStart downloading logos...')
        with open("links.txt", "r") as f:
            links = [link.strip() for link in f]
            unique_links = set(links)
            
            print(len(links))
            print(len(unique_links))
            
        with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
            executor.map(download_logo, links)
     
