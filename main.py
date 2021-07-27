import pandas as pd
from dotenv import load_dotenv
import os
from newsapi import NewsApiClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

my_python_key = os.getenv('API_KEY')
df = pd.read_csv('/Users/hunterpeterson/Downloads/constituents_csv.csv')
news_dict = {

}
newsapi = NewsApiClient(api_key=f'{my_python_key}')
top_headlines = newsapi.get_top_headlines(category='business',
                                          language='en',
                                          country='us')
titles = []
for i in range(0, 20):
    titles.append(top_headlines['articles'][i]['title'] + " " + top_headlines['articles'][i]['description'])

for i in range(0, len(df)):
    for j in range(0, len(titles)):
        if df['Name'][i] in titles[j]:
            news_dict[titles[j]] = df['Name'][i]


def get_sentiment(sentence):
    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(sentence)

    if sentiment_dict['compound'] >= 0.05:
        return "Positive"

    elif sentiment_dict['compound'] <= - 0.05:
        return "Negative"

    else:
        return "Neutral"

stories = []

for i in news_dict:
    stories.append(i)

positive_companies = []
negative_companies = []
print(top_headlines)
print(stories)
for i in range(0, len(stories)):
    prediction = get_sentiment(stories[i])
    print(prediction)
    if prediction == 'Positive':
        is_in = False
        for company in positive_companies:
            if company == news_dict[stories[i]]:
                is_in = True
        if not is_in:
            positive_companies.append(news_dict[stories[i]])
    elif prediction == 'Negative':
        is_in = False
        for company in negative_companies:
            if company == news_dict[stories[i]]:
                is_in = True
        if not is_in:
            negative_companies.append(news_dict[stories[i]])

if len(positive_companies) > 0:
    print(f'These companies were positive in the news: {positive_companies}')
else:
    print('No companies were shown to be positive in the news today.')
if len(negative_companies) > 0:
    print(f'These companies were negative in the news: {negative_companies}')
else:
    print('No companies were shown to be negative in the news today.')
