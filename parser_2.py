from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, TimeoutException
from dotenv import load_dotenv
import time
import random
import os
load_dotenv()

driver = webdriver.Chrome()     #need to download the latest version of chromedriver

def crawl(progress):
    continue_step = progress
    driver.get("https://www.logo-archive.org/")
    print('open')

    wait = WebDriverWait(driver, 10)
    print('waiting...')

    login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Login"]')))
    login_btn.click()
    print('click...')

    # wait for username and password fields to be available
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    username_field.send_keys(os.getenv("account"))
    password_field.send_keys(os.getenv("password"))
    print('info filled...')

    login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-df936f61-0.dnnCYM')))
    login.click()
    print('login...')

    loading_times = 0
    loading_pages = 15
    # loading_pages = 22

    while True:
        try:
            # Try to scroll to the bottom and find the button and click it
            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-df936f61-0.jKZabt')))
            try:
                if loading_times > loading_pages:
                    break
                button.click()
                print(f'page {loading_times}...')
                time.sleep(1.5)
                loading_times+=1
                
            except (ElementClickInterceptedException, StaleElementReferenceException):
                print('retry...')
                continue
            
        except NoSuchElementException:
            break

    # entire wrapper of all logos
    outer_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-3771e24b-0.fAslwK")))
    # each logo
    inner_divs = outer_div.find_elements(By.CSS_SELECTOR, '[aria-label="Open detail view"]')
    print(f'nums of logos = {len(inner_divs)}')
    step_count = 0

    for div_logo in inner_divs:
        if step_count > continue_step:
            
            # if it's story mode
            if div_logo.find_elements(By.CSS_SELECTOR, '.sc-c48c6951-0.goYFGj'):
                
                print('story found!!')
                try:
                    div_logo.click()
                    time.sleep(2)
                    svg_element = driver.find_element(By.CSS_SELECTOR, "div.sc-b733acaa-0.sc-b733acaa-4.kjSvjr.daZidx > div > div > svg")
                    
                    name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-b733acaa-8.jPZqUj')))
                    name_text = name.text.replace("/", "-").replace(" ", "-")
                    
                    tags = driver.find_elements(By.CSS_SELECTOR, 'button.sc-d301294f-0.fgfoIM')                    
                    tags_text = ''
                    for tag in tags:
                        tags_text += '-' + tag.text.replace("/", "-").replace("\n", "-")
                    
                    svg_content = svg_element.get_attribute('outerHTML')
                    file_name = "./logos2/" + name_text + "_" + tags_text + ".svg"
                    print(file_name)
                    with open(file_name, 'w') as svg_file: 
                        svg_file.write(svg_content)
                    
                    print('-----------------')
                    
                    #close overlay
                    close_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-851aada3-0.kCSxnv')))
                    close_btn.click() 
                        
                except Exception as e:
                    print(str(e))
                    print('e')
                    continue
                    
            # if it's normal detail page
            else:
                try:
                    div_logo.click()

                    sleep_time = random.randint(0, 2) 
                    time.sleep(sleep_time)

                    name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-71032f02-4.sc-71032f02-5.clHDhA')))
                    cat = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.sc-71032f02-6.sc-71032f02-7.cZVgpD.cffzqq')))
                    tags = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.sc-71032f02-6.sc-71032f02-8.cZVgpD.klBUhb')))
                    name_text = name.text.replace("/", "-").replace(" ", "-")
                    cat_text = cat.text.replace("/", "-").replace("\n", "-")
                    tags_text = tags.text.replace("/", "-").replace("\n", "-")
                    file_name = "./logos2/" + name_text + "_" + cat_text + "_" + tags_text + ".svg"
                    print(file_name)
                    print('-----------------')
                    
                    # Find the SVG element.
                    # Get the outerHTML attribute, which is the SVG element itself.
                    svg_element = driver.find_element(By.CSS_SELECTOR, 'div.sc-6d93bfb1-1.sc-6d93bfb1-3.hYNa-Dy.iGRDGO > svg')
                    svg_content = svg_element.get_attribute('outerHTML')

                    # Write the SVG content to a file.
                    with open(file_name, 'w') as svg_file:
                        svg_file.write(svg_content)
                    
                    print(f'progress = {step_count}')
                    #close overlay
                    close_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-851aada3-0.duwHaz')))
                    close_btn.click() 
                    print('a')
                    
                except (Exception, TimeoutException, ElementClickInterceptedException) as e:
                    continue_step = step_count + 1
                    try:
                        div_kCSxnv = driver.find_elements(By.CSS_SELECTOR, 'div.sc-851aada3-0.kCSxnv')
                        div_VyByJ = driver.find_elements(By.CSS_SELECTOR, 'div.sc-d1cac8af-1.VyByJ')
                        print('b')
                        if div_kCSxnv:
                            div_kCSxnv[0].click()
                        elif div_VyByJ:
                            div_VyByJ[0].click()
                            
                    except Exception as e:
                        print(str(e))
                        print('c')
                        # if everything failed, restart a new crawling process and skip the current element
                        print(f'crawling failed, continue from step{continue_step}')
                        continue
                
        step_count +=1
        
    # Close the driver
    driver.quit()
    print('done')

continue_step = 0
crawl(continue_step)
