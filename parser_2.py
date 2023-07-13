from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import time
import os
load_dotenv()

driver = webdriver.Chrome()

driver.get("https://www.logo-archive.org/")
print('open')

wait = WebDriverWait(driver, 20)
print('wait')

login_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Login"]')))
login_btn.click()
print('click')

# wait for username and password fields to be available
username_field = wait.until(EC.presence_of_element_located((By.NAME, "email")))
password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))

username_field.send_keys(os.getenv("account"))
password_field.send_keys(os.getenv("password"))
print('filled')

login = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-df936f61-0.dnnCYM')))
login.click()
print('login in')

counter = 0
while True:
    try:
        # Try to scroll to the bottom and find the button and click it
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.sc-df936f61-0.jKZabt')))
        try:
            if counter > 5:
                break
            time.sleep(3)
            button.click()
            print(f'loading {counter}...')
            counter+=1
        except ElementClickInterceptedException:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print('scroll...')
            continue

    except NoSuchElementException:
        break

# Save the page source (HTML) to a file
with open("logo-archive.html", "w") as f:
    f.write(driver.page_source)

# Close the driver
driver.quit()


print('done')


