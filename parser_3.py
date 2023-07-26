import requests
from bs4 import BeautifulSoup
import os


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


# Use BeautifulSoup to parse the page you're interested in
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
            f.write('https://www.logolounge.com/' + logo_href + '\n')

print('done')
