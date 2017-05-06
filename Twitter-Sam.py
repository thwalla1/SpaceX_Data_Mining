import twitter
import json
import textmining
from collections import Counter
from prettytable import PrettyTable
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment


def removeUnicode(text):
    asciiText=""
    for char in text:
        if(ord(char)<128):
            asciiText=asciiText+char

    return asciiText

def main():
    CONSUMER_KEY=""
    CONSUMER_SECRET=""
    OAUTH_TOKEN=""
    OAUTH_TOKEN_SECRET=""

    auth=twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    tw=twitter.Twitter(auth=auth)
    q='@SpaceX'
    count=25

    search_results=tw.search.tweets(q=q, count=count, lang='en')
    statuses=search_results['statuses']

    texts=[]
    words=[]

    print q, "\n=========================================\n"
    for status in statuses:
        vs=vaderSentiment(status["text"].encode('utf-8'))
        print 'User', ':::', status['user']['screen_name']
        print 'Tweet', ':::', status['text'].encode('utf-8')
        print 'Sentiment:::', vs
        print 'Likes:::', status['favorite_count']
        print 'Retweet Count:::', status['retweet_count'], '\n'
        texts.append(removeUnicode(status['text']))
    
    for text in texts:
        for word in text.split():
            words.append(word)

    print 'Lexical Diversity:::', 10*len(set(words))/len(words), '\n'

    cnt=Counter(words)
    pt=PrettyTable(field_names=['Word','Count'])
    srtCnt=sorted(cnt.items(), key=lambda pair: pair[1], reverse=True)
    for kv in srtCnt:
        pt.add_row(kv)

    print '--Frequency Count--'
    print pt, '\n'

    tdm=textmining.TermDocumentMatrix()
    for text in texts:
        tdm.add_doc(text)

    print '\nTerm Document Matrix'
    for row in tdm.rows(cutoff=1):
        print row
            
main()

