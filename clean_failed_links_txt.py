import os

with open('logolounge_scrap_failure.txt', 'r') as f:
    count = 0
    links = f.read().split('\n')
    set = set(links)
    for link in links:
        # print(link)
        count +=1
    print(f'links = {count}')
    print(f'unique links = {len(set)}')