import os
import pickle
import pandas as pd
import re
import datetime
from sklearn.preprocessing import LabelEncoder

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *

from dateutil import tz
UTC = tz.gettz("UTC")

from helper.util import Util

def mk_dataset():
    scraping_data_path = '../data/scraping_data/'
    dataset_path = '../data/dataset/'
    df_tweet_data = Util.data_cancat(scraping_data_path, file_name)

    tweet_kw_list = ['日本', 'go', '2回接種済みだった', '機能停止した', '除染作業', 'と言い出した。', '日本政府は', 'PCR', '大阪の場合は', '病院に入院しているらしい', '各党の第一声']

    print(len(df_tweet_data))
    df_tweet_data = df_tweet_data[~df_tweet_data['kw'].isin(tweet_kw_list)]
    print(len(df_tweet_data))
    df_tweet_data = df_tweet_data[~df_tweet_data.duplicated('id')]
    print(len(df_tweet_data))