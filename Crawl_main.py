import random
from time import sleep
import numpy as np
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException
import pandas as pd   

service = Service('chromedriver.exe')
#Declare browser
driver = webdriver.Chrome(service=service)

#Open URL
driver.get("https://www.lazada.vn/adidas1631618372/?from=wangpu&q=gi%C3%A0y%20nam&rating=1")
sleep(random.randint(5,10))

count=0
all_data = pd.DataFrame()
while(True):
    try:
        count+=1
        print("Crawl page " + str(count))
    #==========GET link/title
        elems = driver.find_elements(By.CSS_SELECTOR, ".RfADt [href]")
        title = [elem.text for elem in elems]
        links = [elem.get_attribute('href') for elem in elems]

    #==========GET price, location
        elems_price = driver.find_elements(By.CSS_SELECTOR,".aBrP0")
        price = [elem_price.text for elem_price in elems_price]

        elems_location = driver.find_elements(By.CSS_SELECTOR,"._6uN7R .oa6ri")
        location =  [elem_location.text for elem_location in elems_location]

        df1 = pd.DataFrame(list(zip(title, price, location, links)), columns=['title', 'price', 'location', 'link_item'])
        df1['index'] = np.arange(1,len(df1)+1)

    #==========GET discount
        price_before_discount, discount_idx, discount_percent_list = [], [], []
        for i in range(1, len(title)+1):
            try:
                discount = driver.find_element("xpath", "/html/body/div[4]/div/div[3]/div[1]/div/div[1]/div[3]/div[{}]/div/div/div[2]/div[4]/span[1]/del".format(i))
                price_before_discount.append(discount.text)
                discount_percent = driver.find_element("xpath", "/html/body/div[4]/div/div[3]/div[1]/div/div[1]/div[3]/div[{}]/div/div/div[2]/div[4]/span[2]".format(i))
                discount_percent_list.append(discount_percent.text)
                print(i)
                discount_idx.append(i)
            except NoSuchElementException:
                print("No Such Element Exception " + str(i))

        df2 = pd.DataFrame(list(zip(discount_idx , price_before_discount, discount_percent_list)), columns = ['discount_idx', 'price_before_discount','discount_percent'])

        df3 = df1.merge(df2, how='left', left_on='index', right_on='discount_idx')

    # #=======GET sold quantity:
        sold_quantity, sold_quantity_idx = [], []
        for i in range(1, len(title)+1):
            try:
                elems_quantity = driver.find_element("xpath","/html/body/div[4]/div/div[3]/div[1]/div/div[1]/div[3]/div[{}]/div/div/div[2]/div[5]/span[1]/span[1]".format(i))
                sold_quantity.append(elems_quantity.text)
                sold_quantity_idx.append(i)
            except NoSuchElementException:
                print("No Such Element Exception " + str(i))
        dfq = pd.DataFrame(list(zip(sold_quantity_idx, sold_quantity)), columns=['sold_quantity_idx', 'sold_quantity'])
        df_final = df3.merge(dfq, how='left', left_on='index', right_on='sold_quantity_idx')
    
    #=======Concat data
        all_data = pd.concat([all_data, df_final], ignore_index=True) 

    #========Next button and exit button
        next_button = driver.find_element(By.CSS_SELECTOR, '.ant-pagination-next')
        next_button.click()
        print("Clicked on next button")
        sleep(random.randint(1,3))
        try:
            close_button = driver.find_element("xpath","/html/body/div[9]/div[2]/div")
            close_button.click()
            print("Click on exit button")
            
            next_button = driver.find_element(By.CSS_SELECTOR, '.ant-pagination-next')
            next_button.click()
            print("Clicked on next button")
            sleep(random.randint(1,3))
        except NoSuchElementException:
            continue
        sleep(random.randint(1,3))
    except ElementNotInteractableException:
        print("Element Not Interactable Exception!")
        break

#Save the final dataframe to a CSV file
all_data.to_csv('raw.csv', index=False)

# Close the browser
#driver.quit()



