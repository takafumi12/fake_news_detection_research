from selenium import webdriver
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd
import time
import os
from helper.util import Util

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options, executable_path=r"./chromedriver")
username = "takafumi89124@gmail.com"
password = "nwf3hdb8"


def nikkei_site_access():
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

def search_news(target_kw):
    volume = 200
    target_url=f'https://r.nikkei.com/search?keyword=sort%3Ascore++{target_kw}&volume={volume}'
    driver.get(target_url)
    time.sleep(5)
    # driver.save_screenshot("ss2.png")
    # driver.find_element_by_class_name('nui-button search__more-button')
    article_number = int(driver.find_element_by_xpath('/html/body/main/div[3]/div/div/div[2]/div[1]/div[1]/div/div/div/p').text.replace(',', ''))
    article_number = 1000
    stop = int((article_number-volume)/10)
    # stop = 10
    for i in range(stop):
        element = driver.find_element_by_xpath('/html/body/main/div[3]/div/div/div[2]/div[3]/button')
        driver.execute_script("arguments[0].click();", element)
        # driver.execute_script("arguments[0].scrollIntoView(false);", element)
        # element.click()
        time.sleep(2)
    return driver.page_source

def scraping_nikkei_news_data(html):
    # BeautifulSoup 
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("h3",attrs={"class":"nui-card__title"})

def get_nikkei_news_data():
    target_kw_list = ['新型コロナウイルス+ワクチン', '新型コロナウイルス+病院']
    nikkei_site_access()
    for target_kw in target_kw_list:
        html = search_news(target_kw)
        sel = scraping_nikkei_news_data(html)
    
        # CSV file output
        out_number = []
        out_url = []
        out_title = []

        for i in range(0, len(sel)):
            out_number.append(str(i))
            out_url.append(sel[i].a.get("href"))
            out_title.append(sel[i].a.get("title"))
    
        resdata = np.vstack([out_number, out_title, out_url])
        df_nikkei_news_title = pd.DataFrame(data=resdata).T
        df_nikkei_news_title.columns = ['number', 'title', 'url']
        df_nikkei_news_title['target_kw'] = target_kw

        # newsのタイトルをlist化してpklで保存
        data_path_pkl = os.path.join('../data', 'scraping_data', 'nikkei_news_data', f'nikkei_news_title_list.pkl')
        nikkei_news_title_list = [re.sub(r'（.*）', '', s) for s in df_nikkei_news_title['title'].tolist()]
        nikkei_news_title_list = [re.sub(r'\[.*\]', '', s) for s in nikkei_news_title_list]
        nikkei_news_title_list = [s for s in nikkei_news_title_list if s != '']
        print(nikkei_news_title_list)
        if os.path.exists(data_path_pkl):
            nikkei_news_title_list_tmp = Util.load(data_path_pkl)
            nikkei_news_title_list = nikkei_news_title_list + nikkei_news_title_list_tmp
            nikkei_news_title_list = list(set(nikkei_news_title_list))
        Util.dump(nikkei_news_title_list , data_path_pkl)

        data_path_csv = os.path.join('../data', 'scraping_data', 'nikkei_news_data', f'nikkei_news_data.csv')
        if os.path.exists(data_path_csv):
            df_nikkei_news_title_tmp = pd.read_csv(data_path_csv)
            df_nikkei_news_title = pd.concat([df_nikkei_news_title, df_nikkei_news_title_tmp], axis=0)
        df_nikkei_news_title.to_csv(data_path_csv, index=False)
        
    driver.quit()

    return data_path_pkl