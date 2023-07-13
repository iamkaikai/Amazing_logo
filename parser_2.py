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

driver = webdriver.Chrome()

driver.get("https://www.logo-archive.org/")
print('open')

wait = WebDriverWait(driver, 20)
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
loading_pages = 23

while True:
    try:
        # Try to scroll to the bottom and find the button and click it
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-df936f61-0.jKZabt')))
        try:
            if loading_times > loading_pages:
                break
            button.click()
            print(f'page {loading_times}...')
            loading_times+=1
            
        except (ElementClickInterceptedException, StaleElementReferenceException):
            print('retry...')
            continue
        
    except NoSuchElementException:
        break


outer_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-3771e24b-0.fAslwK")))
inner_divs = outer_div.find_elements(By.CSS_SELECTOR, '[aria-label="Open detail view"]')

step_count = 0
continue_count = 494

for div_logo in inner_divs:
    if step_count > continue_count:
        try:
            div_logo.click()

            sleep_time = random.randint(1, 4) 
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
                
            #close overlay
            close_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.sc-851aada3-0.duwHaz')))
            close_btn.click() 
            
        except TimeoutException:
            try:
                div_kCSxnv = driver.find_elements(By.CSS_SELECTOR, 'div.sc-851aada3-0.kCSxnv')
                div_VyByJ = driver.find_elements(By.CSS_SELECTOR, 'div.sc-d1cac8af-1.VyByJ')
                
                if div_kCSxnv:
                    div_kCSxnv[0].click()
                elif div_VyByJ:
                    div_VyByJ[0].click()
            except Exception as e:
                print(str(e))
                continue

            continue
        
    step_count +=1
    
# Close the driver
driver.quit()
print('done')


