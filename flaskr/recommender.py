import requests
from flask import jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from reactionrnn import reactionrnn
from . import indiv_models

url = ('https://newsapi.org/v2/top-headlines?country=us&pageSize=100&apiKey=cde202936bf948eeb49767c5b3495493')

def get_recommendations():
    news_resp = requests.get(url)
    news_resp_dict = news_resp.json()
    articles = news_resp_dict['articles']

    return selectorVader(articles)

def selectorReact(articles):
    react = reactionrnn()
    selected = []

    for article in articles:
        labels = react.predict_label(article['content'])
        
        if 'love' in labels:
            selected.append(article)
    
    return selected

def selectorVader(articles):
    analyser = SentimentIntensityAnalyzer()
    scores = []

    for article in articles:
        score = analyser.polarity_scores(article['title'])
        scores.append(score['compound'])
    articles_scores = list(zip(articles, scores))
    sorted_articles_scores = sorted(articles_scores, key=lambda x : x[1], reverse=True)
    
    sorted_articles = [ x[0] for x in sorted_articles_scores ]
    # print([ x[1] for x in sorted_articles_scores ])

    return sorted_articles[:10]

def selectorIndiv(articles):
    indivModel = 
    scores = []

    for article in articles:
        score = indivModel.polarity_scores(article['title'])
        scores.append(score['compound'])
    articles_scores = list(zip(articles, scores))
    sorted_articles_scores = sorted(articles_scores, key=lambda x : x[1], reverse=True)
    
    sorted_articles = [ x[0] for x in sorted_articles_scores ]
    print([ x[1] for x in sorted_articles_scores ])

    return sorted_articles[:10]
    

