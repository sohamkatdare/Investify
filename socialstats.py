import tweepy
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from textblob import TextBlob
from bs4 import BeautifulSoup
import os
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

    f = lambda tweet: TextBlob(tweet).sentiment.polarity # type: ignore
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

# Reimplementing Twitter architecture
def getTweetsFromHTML(html, ticker):
    # We want to retrieve the tweets from the HTML, and get the following information:
    # - Tweet text
    # - Tweet date
    # - Tweet author
    # - Tweet author profile pic
    # - Tweet author verification status
    # - Tweet url
    # - IF image, THEN image_url (could be removed if having some image and some not is bad UI)
    # - Maybe Tweet likes and retweets
    html_test = getHTMLFromFile('example')
    soup = BeautifulSoup(html_test, 'html.parser')
    tweets = soup.find_all('article', attrs={'role': 'article'})
    profile_pic_src = ''
    image_src = ''
    for tweet in tweets:
        images = tweet.find_all('img', attrs={'alt': 'Image', 'class': 'css-9pa8cd'})
        if len(images) > 0:
            profile_pic_src = images[0]['src']
            if len(images) > 1:
                image_src = images[1]['src']
        tweet_link = tweet.find('a', attrs={'role': 'link', 'class': 'css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1pi2tsx r-1ny4l3l'})
        tweet_text_div = tweet.find('div', attrs={'dir': 'auto', 'lang': 'en', 'data-testid': 'tweetText'})
        tweet_text = reconstruct_tweet(tweet_text_div)
        print(tweet_text)
        tweet_author = tweet.find('div', attrs={'data-testid': 'User-Name'}).find('span', attrs={'class': 'css-901oao css-16my406 r-1awozwy r-xoduu5 r-poiln3 r-bcqeeo r-qvutc0'})

    pass

def reconstruct_tweet(tweet_div):
    tweet_text = ''
    for span in tweet_div.find_all('span'):
        if 'css-901oao' in span.get('class', []):
                tweet_text += span.text
        elif 'r-18u37iz' in span.get('class', []):
                a = span.find('a')
                if a and not a['href'].startswith(('http', 'https')):
                    tweet_text += a.text
    if tweet_text.endswith("Show more"):
        tweet_text = tweet_text[:-9].rstrip()
    return tweet_text

def getHTMLFromFile(filename):
    # We want to retrieve the HTML from the file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    html_file_path = os.path.join(script_dir, f'static/test/html/{filename}.html')
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html = file.read()
        # print(html)
        return html
if __name__ == '__main__':
    # print(getSocialStats('MSFT'))
    getTweetsFromHTML('example', 'MSFT')