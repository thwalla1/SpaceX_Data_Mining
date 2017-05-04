import twitter
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

# removes unicode
def removeUnicode(text):
    Text = ""
    for char in text:
        if (ord(char)< 128):
            Text += char
    return Text

# returns lexical diversity
def getLex(text):
    words = text.split()
    return 1.0 * len(set(words))/len(words)

# returns sentiment
def getSent(text):
    vs = vaderSentiment(text.encode("utf-8"))
    return vs["compound"]

# prints out the analysis of the tweet
def analyze(tweet):
    user = tweet["user"]["screen_name"]
    text = removeUnicode(tweet["text"])
    retweets = tweet["retweet_count"] 
    sent = getSent(text)
    lex = getLex(text)
    out = "user: {}, tweet: {}, retweets: {}, sentiment: {}, lexical diversity: {}\n"             
    print(out.format(user, text, retweets, sent, lex))

# searchs for 25 tweets
def getTweets(tw, query):
    return  tw.search.tweets(q = query, count= 25, lang = "en")

def main():
    
    # access credentials here
    access_token = ""
    access_secret = ""
    consumer_key = ""
    consumer_secret = "" 
  
    auth = twitter.OAuth(access_token, access_secret, consumer_key, consumer_secret)
    tw = twitter.Twitter(auth=auth)

    # first batch
    tweets = getTweets(tw, "@spacex")

    print("first batch of tweets")
    for tweet in tweets["statuses"]:
        analyze(tweet)
  
    # second batch
    tweets = getTweets(tw, "@spacex")
    print("second batch of tweets")
    
    for tweet in tweets["statuses"]:
        analyze(tweet)
  

main()

