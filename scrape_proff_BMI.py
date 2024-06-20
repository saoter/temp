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

DRIVER_PATH = 'C:\chromedriver.exe'
driver = webdriver.Chrome()
driver.get('https://www.proff.dk/')



# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]'))).click()
max_retries = 5
for i in range(max_retries):
    try:
        # Wait until the element is clickable
        element = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[3]'))
        )
        # Click the element
        element.click()
        break  # Exit the loop if successful
    except StaleElementReferenceException:
        # Print a message and retry
        print(f"StaleElementReferenceException caught. Retrying {i+1}/{max_retries}...")
        if i == max_retries - 1:
            print("Max retries reached. Exiting.")
            raise  # Re-raise the exception if max retries reached


rev_data = ['15827084', '38358812', '31889480']

time.sleep(2)
df = pd.DataFrame()
for i in rev_data:
    try:
        driver.get('https://www.proff.dk/')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys(i)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys("\n")
        link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "addax-cs_hl_hit_company_name_click")]')))
        link = link.get_attribute('href')
        driver.get(link)

        link2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "AccountFiguresWidget-seeAllLink")]')))
        link2 = link2.get_attribute('href')
        driver.get(link2)
        
        table = pd.read_html(driver.page_source)[1]
        table2 = pd.read_html(driver.page_source)[2] 
        table_antal = pd.read_html(driver.page_source)[3] 
        
        link3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "addax-cs_ip_analysis_click")]')))
        link3 = link3.get_attribute('href')
        driver.get(link3)
        table3 = pd.read_html(driver.page_source)[0]
        table3.rename(columns={ table3.columns[0]: "Nøgletal" }, inplace = True)

        t0 = table.loc[table['RESULTATREGNSKAB'] == 'Primært resultat']
        t1 = table.loc[table['RESULTATREGNSKAB'] == 'Nettoomsætning']
        t2 = table.loc[table['RESULTATREGNSKAB'] == 'Resultat før skat']
        t3 = table.loc[table['RESULTATREGNSKAB'] == 'Anlægsaktiver i alt']
        t4 = table.loc[table['RESULTATREGNSKAB'] == 'Omsætningsaktiver i alt']
        t5 = table2.loc[table2['BALANCEREGNSKAB'] == 'Passiver i alt']

        t6 = table3.loc[table3['Nøgletal'] == 'Dækningsgrad']
        t7 = table3.loc[table3['Nøgletal'] == 'Overskudsgrad']
        t8 = table3.loc[table3['Nøgletal'] == 'Kapacitetsgrad']
        t9 = table3.loc[table3['Nøgletal'] == 'Afkastningsgrad']
        t10 = table3.loc[table3['Nøgletal'] == 'Likviditetsgrad 1']
        t11 = table3.loc[table3['Nøgletal'] == 'Soliditetsgrad i %']
        t12 = table3.loc[table3['Nøgletal'] == 'Egenkapitalens forrentning 1']
        t13 = table_antal.loc[table_antal['ANDET'] == 'Antal ansatte']
        

        t0.columns.values[0] = "variable" 
        t1.columns.values[0] = "variable"   
        t2.columns.values[0] = "variable"        
        t3.columns.values[0] = "variable"        
        t4.columns.values[0] = "variable"      
        t5.columns.values[0] = "variable"        
        t6.columns.values[0] = "variable"     
        t7.columns.values[0] = "variable"   
        t8.columns.values[0] = "variable"        
        t9.columns.values[0] = "variable"        
        t10.columns.values[0] = "variable"      
        t11.columns.values[0] = "variable"        
        t12.columns.values[0] = "variable"    
        t13.columns.values[0] = "variable"    


        t = pd.concat([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], axis=0)
        t = t.iloc[: , :-1]
        t = t.rename(columns=lambda x: x[0 : 13])
        t['Cvr'] = i
        
        df = pd.concat([df, t], ignore_index=True)
        df.to_csv('fin_data.csv', index=False, encoding='utf-8-sig')
    except:
        pass
        driver.get('https://www.proff.dk/')
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys(i)
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Søg efter virksomheder eller personer"]'))).send_keys("\n")
        link = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "addax-cs_hl_hit_company_name_click")]')))
        link = link.get_attribute('href')
        driver.get(link)

        link2 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "AccountFiguresWidget-seeAllLink")]')))
        link2 = link2.get_attribute('href')
        driver.get(link2)
        
        table = pd.read_html(driver.page_source)[1]
        table2 = pd.read_html(driver.page_source)[2] 
        table_antal = pd.read_html(driver.page_source)[3] 
        
        link3 = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//a[contains(@class, "addax-cs_ip_analysis_click")]')))
        link3 = link3.get_attribute('href')
        driver.get(link3)
        table3 = pd.read_html(driver.page_source)[0]
        table3.rename(columns={ table3.columns[0]: "Nøgletal" }, inplace = True)


        t0 = table.loc[table['RESULTATREGNSKAB'] == 'Primært resultat']
        t1 = table.loc[table['RESULTATREGNSKAB'] == 'Nettoomsætning']
        t2 = table.loc[table['RESULTATREGNSKAB'] == 'Resultat før skat']
        t3 = table.loc[table['RESULTATREGNSKAB'] == 'Anlægsaktiver i alt']
        t4 = table.loc[table['RESULTATREGNSKAB'] == 'Omsætningsaktiver i alt']
        t5 = table2.loc[table2['BALANCEREGNSKAB'] == 'Passiver i alt']

        t6 = table3.loc[table3['Nøgletal'] == 'Dækningsgrad']
        t7 = table3.loc[table3['Nøgletal'] == 'Overskudsgrad']
        t8 = table3.loc[table3['Nøgletal'] == 'Kapacitetsgrad']
        t9 = table3.loc[table3['Nøgletal'] == 'Afkastningsgrad']
        t10 = table3.loc[table3['Nøgletal'] == 'Likviditetsgrad 1']
        t11 = table3.loc[table3['Nøgletal'] == 'Soliditetsgrad i %']
        t12 = table3.loc[table3['Nøgletal'] == 'Egenkapitalens forrentning 1']
        t13 = table_antal.loc[table_antal['ANDET'] == 'Antal ansatte']
        

        t0.columns.values[0] = "variable" 
        t1.columns.values[0] = "variable"   
        t2.columns.values[0] = "variable"        
        t3.columns.values[0] = "variable"        
        t4.columns.values[0] = "variable"      
        t5.columns.values[0] = "variable"        
        t6.columns.values[0] = "variable"     
        t7.columns.values[0] = "variable"   
        t8.columns.values[0] = "variable"        
        t9.columns.values[0] = "variable"        
        t10.columns.values[0] = "variable"      
        t11.columns.values[0] = "variable"        
        t12.columns.values[0] = "variable"    
        t13.columns.values[0] = "variable"    


        t = pd.concat([t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13], axis=0)
        t = t.iloc[: , :-1]
        t = t.rename(columns=lambda x: x[0 : 13])
        t['Cvr'] = i
        
        #df = df.append(t)
        df = pd.concat([df, t], ignore_index=True)
        df.to_csv('fin_data.csv', index=False, encoding='utf-8-sig')      


driver.quit()  
