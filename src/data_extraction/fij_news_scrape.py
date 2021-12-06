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

def fake_news_from_fij_scraping(r):
    fake_twitter_text_list = []
    fake_twitter_text_dict = {}
    soup = BeautifulSoup(r.text, "html.parser")
    for a in soup.select('blockquote > p > strong'):
        fake_twitter_text_original = re.sub(r'</?strong>', '', str(a))
        fake_twitter_text = re.sub(r'（.*）', '', fake_twitter_text_original)
        fake_twitter_text = re.sub(r'\(.*）', '', fake_twitter_text)
        fake_twitter_text = re.sub(r'（.*\)', '', fake_twitter_text)
        fake_twitter_text = fake_twitter_text.replace(r'○', '')
        fake_twitter_text = fake_twitter_text.replace(r' ／ ', ' ')
        tmp_list = fake_twitter_text.split()
        fake_twitter_text_dict[fake_twitter_text_original] = tmp_list
        for tmp in tmp_list:
            fake_twitter_text_list.append(tmp)

    print(fake_twitter_text_list)
    print(len(fake_twitter_text_list))

    return fake_twitter_text_list, fake_twitter_text_dict

def get_fake_twitte_data(url):
    r = get_web_page(url)
    fake_twitter_text_list, fake_twitter_text_dict = fake_news_from_fij_scraping(r)
    data_path_list = os.path.join('../data', 'scraping_data', 'fij_news_data',f'fake_twitter_text_list.pkl')
    print(data_path_list)
    Util.dump(fake_twitter_text_list, data_path_list)
    data_path_dict = os.path.join('../data', 'scraping_data', 'fij_news_data',f'fake_twitter_text_dict.pkl')
    Util.dump(fake_twitter_text_dict, data_path_dict)

    return data_path_list
