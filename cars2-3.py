import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

driver = webdriver.Chrome()
driver.get("https://www.cardekho.com/cardealers")

search = "bmw"
wait = WebDriverWait(driver, timeout=3, poll_frequency=1)
time.sleep(2)

dealers = [["Brand" , "Town" , "Phone number" , "Name" , "Adress" , "Showroom time"]]

n = int(input("Choose a number"))

bob = 0

for i in range(n-1,n):
    try:
        buildings = wait.until(EC.presence_of_element_located((By.XPATH,f"(//a[@class='BrIconNewCar'])[{i+1}]")))
        car = buildings.text
        buildings.click()

        time.sleep(0.5)
        buildings = wait.until(EC.presence_of_element_located((By.XPATH,f"(//input[@name='cityDropDown1'])")))
        buildings.click()
        dropdown_list = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='gs_ta_results width100   '])")))

        index = 1
        options = dropdown_list.find_elements(By.TAG_NAME, 'li')

        while len(options) <= index:
            # Send DOWN_ARROW key to scroll through the list
            buildings.send_keys(Keys.DOWN)
            options = dropdown_list.find_elements(By.TAG_NAME, 'li')

        town = options[index].text
        options[index].click()
        but = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//button[@name='go'])")))
        but.click()
        index+=2

        b = 0
        pos = 1
        maxi = 100
        while index < 1622:
            dealer = []
            dealer.append(car)
            dealer.append(town)
            try:

                driver.execute_script(f"window.scrollTo({0}, {340+56*pos});")
                time.sleep(0.8)
                hasPrice = True
                cont = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//ul[@class='fullCtr'])")))
                if pos == 1:
                    li_elements = cont.find_elements(By.TAG_NAME, 'li')
                    maxi = len(li_elements)
                if maxi < pos:
                     aaa = 3 / 0

                try:
                     call = cont.find_element(By.XPATH,f"(//li[{pos}]//div[@class='secondaryButton orangeText'])")
                except:
                     hasPrice = False
                if hasPrice:
                    ps = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='secondaryButton orangeText'])[{pos-bob}]")))
                    ps.click()
                    
                    ps = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='contactNumber'])")))
                    phone = ps.text
                    dealer.append(phone)
                else:
                     bob+=1
                     dealer.append("/")


                ps = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//a[@class='name truncate'])[{pos}]")))
                ps.click()
                pos+=1

                try:
                    time.sleep(1)
                    t1 = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='container '])")))
                    i1 = t1.text
                    dealer.append(i1)
                except:
                    time.sleep(1)
                    t1 = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='container sponsoredc'])")))
                    i1 = t1.text
                    dealer.append(i1)

                t1 = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='cd_address'])")))
                i2 = t1.text
                dealer.append(i2)

                try:
                    t1 = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='showroomtime'])")))
                    i3 = t1.text
                    dealer.append(i3)
                except:
                     dealer.append("/")

                b = 0
                dealers.append(dealer)
                driver.back()
            except Exception as e:
                b +=1
                if b == 2:
                    driver.execute_script(f"window.scrollTo({0}, {150});")
                    time.sleep(2)
                    buildings = wait.until(EC.presence_of_element_located((By.XPATH,f"(//input[@name='cityDropDown1'])")))
                    buildings.click()
                    dropdown_list = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//div[@class='gs_ta_results width100   '])")))
                    options = dropdown_list.find_elements(By.TAG_NAME, 'li')

                    while len(options) <= index:
                        # Send DOWN_ARROW key to scroll through the list
                        buildings.send_keys(Keys.DOWN)
                        options = dropdown_list.find_elements(By.TAG_NAME, 'li')

                    town = options[index].text
                    options[index].click()

                    but = wait.until(EC.visibility_of_element_located((By.XPATH,f"(//button[@name='go'])")))
                    but.click()
                    index+=1
                    if index in [11, 16,25,31,37,46]:
                         index+=1
                    pos = 1
                    b = 0
                    bob = 0
                    with open(f'dealers{n}.csv', 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerows(dealers)
        
        driver.back()

        
        time.sleep(0.5)
        driver.get("https://www.cardekho.com/cardealers")
    except Exception as e:
        time.sleep(1)
        driver.execute_script(f"window.scrollBy({0}, {200});")
        i-=1

with open(f'dealers{n}.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(dealers)

print("Matrix saved to 'matrix.csv'")

driver.quit()