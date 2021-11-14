from data_extraction import fake_news_scrape, tweet_search, nikkei_news_scrape
from helper import util

if __name__ == '__main__':

    # fij_url = 'https://fij.info/coronavirus-feature/national'
    # input_data_path = fake_news_scrape.get_fake_twitte_data(fij_url)
    # tweet_search.get_twitter_data(input_data_path, output_data_dir='fij_news_data')

    input_data_path = nikkei_news_scrape.get_nikkei_news_data()
    tweet_search.get_twitter_data(input_data_path, output_data_dir='nikkei_news_data')