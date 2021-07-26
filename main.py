import pandas as pd
from dotenv import load_dotenv
import os
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from newsapi import NewsApiClient
load_dotenv()

my_python_key = os.getenv('API_KEY')
df = pd.read_csv('/Users/hunterpeterson/Downloads/constituents_csv.csv')
sentiment_df = pd.read_csv('/Users/hunterpeterson/Downloads/archive/all-data.csv', encoding='ISO-8859-1', names=['Sentiment', 'Headline'])
news_dict = {

}
newsapi = NewsApiClient(api_key=f'{my_python_key}')
top_headlines = newsapi.get_top_headlines(category='business',
                                          language='en',
                                          country='us')
titles = []
for i in range(0, 20):
    titles.append(top_headlines['articles'][i]['title'])

for i in range(0, len(df)):
    for j in range(0, len(titles)):
        if df['Name'][i].lower() in titles[j].lower():
            news_dict[titles[j]] = df['Name'][i]

categories = ['neutral', 'negative', 'positive']
y = sentiment_df['Sentiment']
x = sentiment_df['Headline']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = make_pipeline(TfidfVectorizer(), MultinomialNB())

model.fit(x_train, y_train)

labels = model.predict(x_test)

stories = []
for i in news_dict:
    stories.append(i)

for i in range(0, len(stories)):
    stories[i] = [stories[i]]

positive_companies = []
negative_companies = []
print(stories)
for i in range(0, len(stories)):
    prediction = model.predict(stories[i])
    print(prediction)
    if prediction == 'positive':
        is_in = False
        for company in positive_companies:
            if company == news_dict[stories[i]]:
                is_in = True
        if not is_in:
            positive_companies.append(news_dict[stories[i]])
    elif prediction == 'negative':
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
