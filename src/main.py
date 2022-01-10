from data_extraction import fij_news_scrape, tweet_search, nikkei_news_scrape, infact_news_scrape
from helper import util
import argparse

def original_kw(value, tweet_text_dict):
    """
    元のKWを付与
    """
    return [k for k, v in tweet_text_dict.items() if value in v][0]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='データ処理')
    
    parser.add_argument('-e', '--data_extraction_flg', action='store_true', help='データ収集処理フラグ')
    parser.add_argument('-s', '--target_select', type=str, default=None, help='データ収集対象選択')
    parser.add_argument('-t', '--model_train_flg', action='store_true', help='モデル学習フラグ')

    args = parser.parse_args()

    if args.data_extraction_flg:
        if args.target_select == 'fij':
            fij_url = 'https://fij.info/coronavirus-feature/national'
            input_data_path = fij_news_scrape.get_fake_twitte_data(fij_url)
            tweet_search.get_twitter_data(input_data_path, output_data_dir='fij_news_data')
        
        elif args.target_select == 'infact':
            infact_url = 'https://infact.press/tag/covid-19-factchecks/'
            input_data_path = infact_news_scrape.get_fake_twitte_data(infact_url)
            tweet_search.get_twitter_data(input_data_path, output_data_dir='infact_news_data')

        elif args.target_select == 'nikkei':
            input_data_path = nikkei_news_scrape.get_nikkei_news_data()
            tweet_search.get_twitter_data(input_data_path, output_data_dir='nikkei_news_data')

    if args.model_train_flg:
        