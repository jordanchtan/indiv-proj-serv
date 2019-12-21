import requests
from flask import jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

url = ('https://newsapi.org/v2/top-headlines?country=us&pageSize=100&apiKey=cde202936bf948eeb49767c5b3495493')

def get_recommendations():
    news_resp = requests.get(url)
    news_resp_dict = news_resp.json()
    articles = news_resp_dict['articles']

    return selector(articles)

def selector(articles):
    analyser = SentimentIntensityAnalyzer()
    selected = []

    for article in articles:
        score = analyser.polarity_scores(article['title'])
        if score['compound'] > 0.5:
            selected.append(article)
    
    return selected

