import requests
from flask import jsonify
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# from reactionrnn import reactionrnn
from . import indiv_models


class Recommender:

    def __init__(self):
        print("init recommender")
        self.model = indiv_models.PositiveRatioModel()

    def get_recommendations(self):
        articles = []
        sources = ['abc-news']
        # sources = ['abc-news', 'bbc-news', 'cbs-news', 'cnn', 'fox-news', 'nbc-news', 'the-huffington-post', 'the-wall-street-journal',
        #            'the-washington-post',
        #            'time',
        #            'usa-today']
        for src in sources:
            news_resp = requests.get('https://newsapi.org/v2/everything?sources=' +
                                     src + '&pageSize=100&apiKey=cde202936bf948eeb49767c5b3495493')
            news_resp_dict = news_resp.json()
            arts = news_resp_dict['articles']
            articles = articles + arts

        return self.selectorIndiv(articles)
    #  https://newsapi.org/v2/everything?sources=cnn&pageSize=100&apiKey=cde202936bf948eeb49767c5b3495493

    # def selectorReact(self, articles):
    #     react = reactionrnn()
    #     selected = []

    #     for article in articles:
    #         labels = react.predict_label(article['content'])

    #         if 'love' in labels:
    #             selected.append(article)

    #     return selected

    # def selectorVader(self, articles):
    #     analyser = SentimentIntensityAnalyzer()
    #     scores = []

    #     for article in articles:
    #         score = analyser.polarity_scores(article['title'])
    #         scores.append(score['compound'])
    #     articles_scores = list(zip(articles, scores))
    #     sorted_articles_scores = sorted(
    #         articles_scores, key=lambda x: x[1], reverse=True)

    #     sorted_articles = [x[0] for x in sorted_articles_scores]
    #     # print([ x[1] for x in sorted_articles_scores ])

    #     return sorted_articles[:10]

    def selectorIndiv(self, articles):
        # model = indiv_models.PositiveRatioModel()
        scores = []
        for article in articles:
            score = self.model.predict([article])
            scores.append(score[0])

        # scores = self.model.predict(articles)

        articles_scores = list(zip(articles, scores))
        sorted_articles_scores = sorted(
            articles_scores, key=lambda x: x[1], reverse=True)

        sorted_articles = [x[0] for x in sorted_articles_scores]
        print([x[0]['title'] for x in sorted_articles_scores])
        print([x[1] for x in sorted_articles_scores])

        return sorted_articles[:10]
