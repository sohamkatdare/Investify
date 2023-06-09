import tweepy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from textblob import TextBlob
# from wordcloud import WordCloud, STOPWORDS

matplotlib.use('Agg')

def getSocialStats(ticker):
    plt.style.use('dark_background')

    consumer_key = "EPYMAG7GmiaSi44IleswgtFYP"
    consumer_secret = "DzUoLxV3aVkC9nQcsqzL5Vv9G90yyNqVyKT09U656pWrwRKSkk"
    access_token = "1667261040294350864-IdZXuqSepncmdaCnmuCsEUCfQwmgKK"
    access_token_secret = "Zut62J8rMLZovoMi8hRVkKJeh5VDhgkIxURKd8gYDYl1N"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    user = api.verify_credentials()
    print(user.name)
    
    tweets = api.search_tweets(q=f'${ticker} filter:verified', lang='en', count=200)

    print("Number of tweets extracted: {}. \n".format(len(tweets)))

    # for tweet in tweets[:5]:
    #     print(tweet.text)

    own_tweets = [tweet for tweet in tweets if tweet.retweeted == False and "RT @" not in tweet.text and tweet.author.name != "Nour Trades 🧘‍♂️"]
    # print('\n\n\nOwn Tweets')
    # for tweet in own_tweets[:6]:
    #     if tweet.author == "Nour Trades":
            


    df = pd.DataFrame(data=[[tweet.created_at, tweet.text, len(tweet.text), tweet.id, tweet.favorite_count, tweet.retweet_count] for tweet in own_tweets], columns=['Date', 'Tweet', 'Length', 'ID', 'Likes', 'Retweets'])

    f = lambda tweet: TextBlob(tweet).sentiment.polarity
    df['Sentiment'] = df['Tweet'].apply(f)
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # # print(df.head())
    fig = plt.figure()
    ax = df['Sentiment'].plot(kind='hist', bins=20, figsize=(5,5), ec='black', color=(30/255, 184/255, 84/255, 0.6))
    ax.set_facecolor('#171212')
    ax.set_xlabel('Sentiment')
    ax.set_ylabel('Frequency')
    ax.set_title('Sentiment of Tweets (Histogram)')
    fig.tight_layout()
    fig.savefig('static/SentimentOfTweets.png', facecolor=plt.gca().get_facecolor())
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

    text = " ".join(text for text in df.Tweet)

    stopwords = set({'until', 'do', 'why', "we'll", 'there', 'in', 'all', "why's", "i'm", 'r', "hadn't", 'because', 'from', 'you', 'yourselves', 'few', 'himself', 'as', 'about', 'these', 'where', 'other', 'hers', 'above', 'being', 'further', 'through', 'therefore', "mustn't", "they've", 'com', 'into', 'not', 'itself', 'out', 'ought', "can't", 'ever', "it's", "you'll", 'while', 'get', "he's", "isn't", 'themselves', 'just', 'should', 'ourselves', 'can', 'shall', "here's", "when's", 'a', 'them', 'they', 'and', 'own', 'she', "they'll", 'like', 'off', 'http', 'or', 'been', "hasn't", 'herself', 'whom', 'no', "wasn't", "you've", 'how', "they're", 'me', 'nor', 'before', 'did', "she'll", "i'd", "she'd", "you'd", 'at', 'below', 'hence', 'otherwise', "weren't", 'when', 'having', 'more', 'cannot', "we've", 'such', 'him', "where's", 'who', 'than', 'between', 'k', 'since', 'their', 'am', 'the', 'it', 'then', 'same', 'of', 'any', 'once', 'those', 'we', 'are', 'else', 'very', 'theirs', 'your', "we're", "won't", 'has', 'had', "they'd", "how's", 'under', 'down', 'were', "wouldn't", 'here', 'up', "he'll", 'each', "don't", 'against', "let's", 'over', 'most', 'after', 'its', 'on', "couldn't", "i'll", 'i', 'my', 'during', 'both', "doesn't", 'for', 'he', "shouldn't", 'so', 'if', 'again', 'does', 'doing', 'our', "didn't", 'myself', 'only', "shan't", 'www', 'that', "who's", 'was', "she's", "he'd", 'yourself', "you're", 'his', 'some', 'with', 'too', 'is', 'have', 'her', "i've", 'to', 'which', 'by', "haven't", 'would', 'what', 'an', "what's", 'be', 'ours', 'could', "that's", "aren't", "there's", 'also', 'yours', 'but', 'however', 'this', "we'd"})
    stopwords.update(["HTTPS", "CO", 'T', 'H'])

    # wordcloud = WordCloud(stopwords=stopwords, background_color="#171212").generate(text)

    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.tight_layout()
    # plt.savefig('static/wordcloud.png', facecolor=plt.gca().get_facecolor())
    # # plt.show()

    return [i for i in own_tweets if len(i.text.split(' ')) > 15][:6], df, df.loc[:, 'Sentiment'].mean()

if __name__ == '__main__':
    print(getSocialStats('MSFT'))