import queue
import requests
from concurrent.futures import ThreadPoolExecutor
import threading
from dotenv import load_dotenv
import os

load_dotenv()
proxy_user = os.getenv('proxy_user')
proxy_password = os.getenv('proxy_password')
print(proxy_user)
print(proxy_password)

q = queue.Queue()
valid_proxies = []
proxy_lock = threading.Lock()

with open('proxies.txt', 'r') as f:
    proxies = f.read().split('\n')
    for p in proxies:
        q.put(p)



def check_proxies(dummy_arg):
    global q
    while not q.empty():
        proxy = q.get()
        proxies_dict = {
            'http': f"http://{proxy_user}:{proxy_password}@{proxy}",
            'https': f"https://{proxy_user}:{proxy_password}@{proxy}", 
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
        }
        print(proxies_dict)
        try:
            res = requests.get('https://icanhazip.com/', proxies=proxies_dict, headers=headers, timeout=1) # Change the endpoint to example.com
            if res.status_code == 200:
                print("Your actual IP:", res.text.strip())
                print(f'proxy {proxies_dict} succeed! Status code: {res.status_code}')
                with proxy_lock:  # Use a lock to safely append to the list
                    valid_proxies.append(proxy)
            else:
                print(f'proxy {proxy} failed with status code: {res.status_code}')
        except requests.RequestException as e:
            print(f'something wrong with proxy {proxy}. Error: {e}')
            continue

with ThreadPoolExecutor(max_workers=1) as executor:
    executor.map(check_proxies, range(1))

print(f"Valid proxies: {valid_proxies}")

