import time
import requests
import os
import datetime
import json
import pandas as pd
from helper.util import Util

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
# bearer_token = os.environ.get("BEARER_TOKEN")
bearer_token = "AAAAAAAAAAAAAAAAAAAAAIr7UwEAAAAAk8ockdCDUU9S%2FH0OrtqrOcoDOXk%3Dhfn84YClegRdTGDXVmrnmz3eGSkTjHydgUdEVIBeXuJzB3xalG"

search_url = "https://api.twitter.com/2/tweets/search/all"

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {
    'query': '',
    'start_time':'2019-01-01T00:00:00Z',
    'tweet.fields': 'conversation_id,in_reply_to_user_id,author_id,created_at',
    'max_results':100}


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FullArchiveSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_twitter_data(data_path):
    target_list = Util.load(data_path)
    # df = pd.DataFrame(colums=['text', 'author_id', 'conversation_id', 'id', 'created_at', 'in_reply_to_user_id'])

    df = None

    for target in target_list:
        print(target)
        query_params['query'] = target
        print(query_params)
        json_response = connect_to_endpoint(search_url, query_params)
        time.sleep(1)
        print(json.dumps(json_response, indent=4, sort_keys=True, ensure_ascii=False))
        if json_response['meta']['result_count'] != 0:
            df_tmp = pd.json_normalize(json_response['data'])

            if df is None:
                df = df_tmp
            else:
                df = pd.concat([df, df_tmp])
        else:
            pass
    data_path = os.path.join('../data', f'{datetime.date.today()}', 'scrapring_data', f'fake_twitter_text_list.pkl')
    Util.dump(df, data_path)
    df.to_csv('/Users/kanekotakafumi/github/fake_news_detection_research/data/tweet_data/tweet_data.csv',  index=False)