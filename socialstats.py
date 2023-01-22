# import tweepy
# import pandas as pd
# import matplotlib
# import matplotlib.pyplot as plt
# from textblob import TextBlob
# from wordcloud import WordCloud, STOPWORDS

# matplotlib.use('Agg')

def getSocialStats(ticker):
    # plt.style.use('dark_background')

    # consumer_key = "44GowZTEx9UJyVAt1Re2qUZTE"
    # consumer_secret = "npEIqH5c2lIojIYOCDeSFbk0r0QDM9h4kxkxNe5zqkhY8hs6UE"
    # access_token = "1411679681393434628-irZ7HTOgXyloLL7t1w7kpUyl3mjI7u"
    # access_token_secret = "594smzKprI4VT0kvlqSnuZZr5at538uZpnyKT04UMKgIR"

    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth)

    # user = api.verify_credentials()
    # print(user.name)
    
    # tweets = api.search_tweets(q=f'${ticker} filter:verified', lang='en', count=200)

    # print("Number of tweets extracted: {}. \n".format(len(tweets)))

    # # for tweet in tweets[:5]:
    # #     print(tweet.text)

    # own_tweets = [tweet for tweet in tweets if tweet.retweeted == False and "RT @" not in tweet.text]
    # # print('\n\n\nOwn Tweets')
    # # for tweet in own_tweets[:5]:
    # #     print(tweet.text)

    # df = pd.DataFrame(data=[[tweet.created_at, tweet.text, len(tweet.text), tweet.id, tweet.favorite_count, tweet.retweet_count] for tweet in own_tweets], columns=['Date', 'Tweet', 'Length', 'ID', 'Likes', 'Retweets'])

    # f = lambda tweet: TextBlob(tweet).sentiment.polarity
    # df['Sentiment'] = df['Tweet'].apply(f)
    # df['Date'] = pd.to_datetime(df['Date']).dt.date

    # # print(df.head())
    # fig = plt.figure()
    # ax = df['Sentiment'].plot(kind='hist', bins=20, figsize=(5,5), ec='black', color=(30/255, 184/255, 84/255, 0.6))
    # ax.set_facecolor('#171212')
    # ax.set_xlabel('Sentiment')
    # ax.set_ylabel('Frequency')
    # ax.set_title('Sentiment of Tweets (Histogram)')
    # fig.tight_layout()
    # fig.savefig('static/SentimentOfTweets.png', facecolor=plt.gca().get_facecolor())
    # # plt.show()

    # # date_df = df.groupby(['Date']).mean().reset_index()
    # # print(date_df.head())
    # # date_df.plot(kind='line', x='Date', y='Sentiment', ylim=[-1,1])
    # # plt.axhline(y=0, color='black')
    # # plt.ylabel('Average Sentiment')
    # # plt.title('Daily Average Sentiment of Tweets')
    # # plt.tight_layout()
    # # plt.savefig('static/AverageSentiment.png')
    # # plt.show()

    # text = " ".join(text for text in df.Tweet)

    # stopwords = set(STOPWORDS)
    # stopwords.update(["HTTPS", "CO", 'T', 'H'])

    # wordcloud = WordCloud(stopwords=stopwords, background_color="#171212").generate(text)

    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.tight_layout()
    # plt.savefig('static/wordcloud.png', facecolor=plt.gca().get_facecolor())
    # # plt.show()

    # return [i for i in own_tweets if len(i.text.split(' ')) > 15][:5], df.loc[:, 'Sentiment'].mean()
    return 'hello'

if __name__ == '__main__':
    print(getSocialStats('MSFT'))