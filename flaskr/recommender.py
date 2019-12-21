import requests
from flask import jsonify

url = ('https://newsapi.org/v2/top-headlines?country=us&pageSize=100&apiKey=cde202936bf948eeb49767c5b3495493')

def get_recommendations():
    news_resp = requests.get(url)
    news_resp_dict = news_resp.json()
    articles = news_resp_dict['articles']

    return selector(articles)

def selector(articles):
    return articles[:10]

