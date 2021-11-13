from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=r"./chromedriver")
username = "takafumi89124@gmail.com"
password = "nwf3hdb8"
  
# Login Page
driver.get('https://r.nikkei.com/login')
time.sleep(2)
# driver.save_screenshot("ss1.png")
 
login_username = driver.find_element_by_id("LA7010Form01:LA7010Email")
login_username.clear()
login_username.send_keys(username) 
login_password = driver.find_element_by_id("LA7010Form01:LA7010Password")
login_password.clear()
login_password.send_keys(password)
driver.find_element_by_class_name('btnM1').click()  # Login button click 
time.sleep(2)
driver.save_screenshot("ss2.png")
 
# Search word (ex. IoT, 200 articles)
target_url='https://r.nikkei.com/search...(cut)...IoT&volume=200'
driver.get(target_url)
time.sleep(5)
html = driver.page_source
  
# BeautifulSoup 
soup = BeautifulSoup(html, 'html.parser')
sel = soup.find_all("h3",attrs={"class":"nui-card__title"})
 
# CSV file output
out_number = []
out_url = []
out_title = []
 
for i in range(0, len(sel)):
    out_number.append(str(i))
    out_url.append(sel[i].a.get("href"))
    out_title.append(sel[i].a.get("title"))
 
resdata = np.vstack([out_number, out_title, out_url])
df = pd.DataFrame(data=resdata).T
df.to_csv('result.csv', header=False, index=False)
 
driver.quit()