from data_extraction import fake_news_scrape, tweet_search
from helper import util

if __name__ == '__main__':

    fij_url = 'https://fij.info/coronavirus-feature/national'
    data_path = fake_news_scrape.get_fake_twitte_data(fij_url)
    tweet_search.get_twitter_data(data_path)