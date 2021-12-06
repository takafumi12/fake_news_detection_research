import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from helper.util import Util

def get_web_page(url):
    # url = sys.argv[1]  # 第1引数からURLを取得する。
    r = requests.get(url)  # URLで指定したWebページを取得する。
    r.encoding = r.apparent_encoding  # バイト列の特徴から推定したエンコーディングを使用する。
    print(f'encoding: {r.encoding}', file=sys.stderr)  # エンコーディングを標準エラー出力に出力する。
    print(r.text)  # デコードしたレスポンスボディを標準出力に出力する。
    # f = open('/Users/kanekotakafumi/github/fake_news_detection_research/data/scraping_data/tmp.txt', 'w')
    # f.writelines(r.text)
    # f.close()
    return r

def link_from_infact_scraping(r):
    link_list = []
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.select("div[class='loop-post-thumb normal'] > a"):
        url = a.get('href')
        link_list.append(url)
    
    if not soup.select("link[rel='next']"):
        return link_list
    else:
        next_link = soup.select("link[rel='next']")[0].get('href')
        r = get_web_page(next_link)
        return link_list + link_from_infact_scraping(r)

def fake_news_from_infact_scraping(r, text_list):
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.select("meta[property='og:title']")
    
    print(str(text))
    pattern = '「.*」'

    repatter = re.compile(pattern)
    result = repatter.search(str(text))
    if result is not None:
        result = result.group()
        result = result.replace(r'「', '').replace(r'」', '').replace(r'◉', '')
        text_list.append(result)
        
    text = soup.select("div[class='box-red']")
    print(str(text))
    
    if text is not None:
        pattern = '<div.*?>|</div>|<span.*?>|</span>|<a.*?>.*?</a>|<br/>|</?strong>|（.*）|\(.*|\[.*|\]|<p>.*|</p>'
        result = re.sub(pattern, '', str(text))
        result = result.replace('、',' ').replace(r'◉', '')
        result_list = [s for s in result.split() if not s.startswith('#') and s != '「……」']
        
        for result in result_list:
            text_list.append(result)
            
    return text_list

def get_fake_twitte_data(url):
    r = get_web_page(url)
    link_list = link_from_infact_scraping(r)
    fake_twitter_text_list = []
    for link in link_list:
        r = get_web_page(link)
        fake_twitter_text_list = fake_news_from_infact_scraping(r, fake_twitter_text_list)
    data_path = os.path.join('../data', 'scraping_data', 'infact_news_data',f'fake_twitter_text_list.pkl')
    print(data_path)
    Util.dump(fake_twitter_text_list, data_path)

    return data_path
