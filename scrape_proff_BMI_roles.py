from os import chdir
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")

#chrome to stay open
option.add_experimental_option("detach", True)

# Function for extracting roles and names
def extract_all_table_data(sections):
    table_data = []
    for section in sections:
        rows = section.find_elements(By.XPATH, './/table/tbody/tr')
        for row in rows:
            try:
                rolle = row.find_element(By.XPATH, './/td[1]').text
                navn = row.find_element(By.XPATH, './/td[2]').text
            except:
                rolle = row.find_element(By.XPATH, './/p').text
                navn = row.find_element(By.XPATH, './/a').text
            table_data.append((rolle, navn))
    return table_data


DRIVER_PATH = 'C:\chromedriver.exe'
driver = webdriver.Chrome()
driver.get('https://www.proff.dk/')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]'))).click()
rev_data = ['15827084', '38358812', '31889480']

time.sleep(2)
df = pd.DataFrame(columns=['Cvr', 'role', 'name'])

for i in rev_data:
    try:
        driver.get('https://www.proff.dk/')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys(i)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys("\n")
        link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "addax-cs_hl_hit_company_name_click")]')))
        link = link.get_attribute('href')
        driver.get(link)


        link2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@role="tab" and contains(@class, "addax-cs_ip_company_roles")]')))
        link2 = link2.get_attribute('href')
        driver.get(link2)

        # Wait for the table sections to be present
        table_sections = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MuiTableContainer-root mui-oinz44"]'))
        )

        # Extract data from all tables
        table_data = extract_all_table_data(table_sections)


        # Create a DataFrame for the table data
        dft = pd.DataFrame(table_data, columns=['role', 'name'])

        # Add the company identifier column
        dft['Cvr'] = i

        # Reorder columns to have 'Cvr' as the first column
        dft = dft[['Cvr', 'role', 'name']]
        print(dft)
        df = df.append(dft)
    except:
        driver.get('https://www.proff.dk/')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys(i)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys("\n")
        link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "addax-cs_hl_hit_company_name_click")]')))
        link = link.get_attribute('href')
        driver.get(link)


        link2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[@role="tab" and contains(@class, "addax-cs_ip_company_roles")]')))
        link2 = link2.get_attribute('href')
        driver.get(link2)

        # Wait for the table sections to be present
        table_sections = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[@class="MuiTableContainer-root mui-oinz44"]'))
        )

        # Extract data from all tables
        table_data = extract_all_table_data(table_sections)


        # Create a DataFrame for the table data
        dft = pd.DataFrame(table_data, columns=['role', 'name'])

        # Add the company identifier column
        dft['Cvr'] = i

        # Reorder columns to have 'Cvr' as the first column
        dft = dft[['Cvr', 'role', 'name']]

        df = df.append(dft)
        
driver.quit()  

df = df[df['role'].str.strip().astype(bool)]
df.to_csv('roles_data.csv', index=False, encoding='utf-8-sig')      

