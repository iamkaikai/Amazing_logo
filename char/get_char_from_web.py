from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, time, csv, re
from selenium.common.exceptions import TimeoutException


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Directory for saving images
output_dir = './adobe_font'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
urls = [
    ['Sans Serif', 96,'https://fonts.adobe.com/fonts?browse_mode=default&cc=true&filters=cl:ss&hide_images=true&languages=en&max_styles=26&min_styles=1&ref=tk.com&referrer=0189d50fcf'],
    ['Serif', 47, 'https://fonts.adobe.com/fonts?browse_mode=default&cc=true&filters=cl:se&hide_images=true&languages=en&max_styles=26&min_styles=1&ref=tk.com&referrer=0189d50fcf'],
    ['Slab Serif', 14,'https://fonts.adobe.com/fonts?browse_mode=default&cc=true&filters=cl:sl&hide_images=true&languages=en&max_styles=26&min_styles=1&ref=tk.com&referrer=0189d50fcf'],
    ['Script', 31,'https://fonts.adobe.com/fonts?browse_mode=default&cc=true&filters=cl:sc&hide_images=true&languages=en&max_styles=26&min_styles=1&ref=tk.com&referrer=0189d50fcf'],
    ['Mono', 7,'https://fonts.adobe.com/fonts?browse_mode=default&cc=true&filters=cl:ms&hide_images=true&languages=en&max_styles=26&min_styles=1&ref=tk.com&referrer=0189d50fcf'],
    ['Hand', 14,'https://fonts.adobe.com/fonts?browse_mode=default&cc=true&filters=cl:hm&hide_images=true&languages=en&max_styles=26&min_styles=1&ref=tk.com&referrer=0189d50fcf'],
]
    
with open(f'{output_dir}/metadata.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['File', 'Font Name', 'Font Style', 'Foundry', 'Case', 'Value'])
    
    wait_time = 0.5
    wait = WebDriverWait(driver, wait_time)
    keys = {
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ": "Uppercase",
        "abcdefghijklmnopqrstuvwxyz": "Lowercase"
    }
    

    for style, max_pages, base_url in urls:
        for page_number in range(1, max_pages + 1):
            # Construct and navigate to the page URL
            page_url = re.sub(r'page=\d+', f'page={page_number}', base_url)
            driver.get(page_url)
            for string, letterCase in keys.items():
                # Wait and interact with the input field and list view button
                if page_number == 1:
                    input_field = wait.until(EC.element_to_be_clickable((By.ID, "adobe-fonts-sample-text-field")))
                    input_field.clear()
                    input_field.send_keys(string)
                    list_view_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='List view']")))
                    list_view_button.click()

                # Wait for elements to load
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, 'span.spectrum-Heading--display.ng-binding.ng-isolate-scope.display-in-font--loaded')
                    font_names = driver.find_elements(By.CSS_SELECTOR, '.adobe-fonts-family-card--wide-view .adobe-fonts-family-card__family_name.ng-binding')
                    typefoundries = driver.find_elements(By.CSS_SELECTOR, '.adobe-fonts-family-card--wide-view span.adobe-fonts-family-card__foundry_name.ng-binding')

                    print(f"Found {len(elements)} elements, {len(font_names)} font names, {len(typefoundries)} foundries")

                    for element, font_name, typefoundry in zip(elements, font_names, typefoundries):
                        filename = f'{style}_{font_name.text}_{page_number}_{letterCase}.png'
                        print('\n')
                        print(filename)
                        print(font_name.text)
                        print(typefoundry.text)
                        time.sleep(0.3)
                        element.screenshot(f'{output_dir}/{filename}')
                        csvwriter.writerow([filename, font_name.text, style, typefoundry.text, letterCase, string])
                except TimeoutException:
                    print(f"Somthing wrong with: style: {style}; page: {page_number}; font: {font_name}")
                    continue
        

# Close the driver
driver.quit()