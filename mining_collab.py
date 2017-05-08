print "Importing Packages..."

import requests
import json
import codecs
import Russell
import nltk
from nltk import BigramAssocMeasures
from bs4 import BeautifulSoup
import twitter
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

#=CONSTANTS AND COMMON FUNCTIONS=========================================

STOPWORDS = ["and","to","the","for","in","of","that","a","on","is","get",
"says","you","has","as","at","are","an","with","will","not","have","would",
"so","but","be","like","if","should","always","also","there","or","by","per",
"need","tells","based","use","[","]",";",":","'s","\"","'","''",",",".",
"' "," '","`","``","-","--"," ","  "]

#removeUnicode - Extracts and returns ASCII text
def removeUnicode(text):
	asciiText = ""
	for char in text:
		if(ord(char) < 128):
			asciiText = asciiText + char

	return asciiText

#getDiversity - Returns Lexical Diversity
def getDiversity(text):
	words = text.split()
	return 1.0 * len(set(words))/len(words)

#getSentiment - Returns text Sentiment
def getSentiment(text):
	vs = vaderSentiment(text.encode("utf-8"))
	return vs["compound"]

#=TWITTER MINING FUNCTIONS===============================================

#twAnalyze - Prints analysis of given tweet
def twAnalyze(tweet):
	user = tweet["user"]["screen_name"]
	text = removeUnicode(tweet["text"])
	retweets = tweet["retweet_count"]
	sentiment = getSentiment(text)
	diversity = getDiversity(text)
	out = "user:\t{}\ntweet:\t{}\nretweets: {}, sentiment: {}, lexical diversity: {}\n"
	print(out.format(user, text, retweets, sentiment, diversity))
	return retweets, sentiment, diversity

#getTweets - Retrieves n tweets from Twitter
def getTweets(tw, query, n):
	return  tw.search.tweets(q = query, count = n, lang = "en")

#connTwitter - Returns Twitter connection
def connTwitter(twOA_TOKEN,twOA_SECRET,twCONSUMER_KEY,twCONSUMER_SECRET):
	oAuth = twitter.OAuth(twOA_TOKEN,twOA_SECRET,twCONSUMER_KEY,twCONSUMER_SECRET)
	tw = twitter.Twitter(auth = oAuth)
	return tw

#mineTwitter - Performs batch mining and analysis
def mineTwitter(twConn,twAt,twCount):

	#Retrieve First Tweet Batch
	tweets = getTweets(twConn,twAt,twCount)
	batch1_retweets = []
	batch1_sentiment = []
	batch1_diversity = []

	print("First Tweet Batch")
	for tweet in tweets["statuses"]:
		retweets, sentiment, diversity = twAnalyze(tweet)
		batch1_retweets.append(retweets)
		batch1_sentiment.append(sentiment)
		batch1_diversity.append(diversity)

	#Retrieve Second Tweet Batch
	tweets = getTweets(twConn,twAt,twCount)
	batch2_retweets = []
	batch2_sentiment = []
	batch2_diversity = []

	print("Second Tweet Batch")
	for tweet in tweets["statuses"]:
		retweets, sentiment, diversity = twAnalyze(tweet)
		batch2_retweets.append(retweets)
		batch2_sentiment.append(sentiment)
		batch2_diversity.append(diversity)

	#Batch Analysis
	print "First Batch Statistics:"
	avg_retweets = sum(batch1_retweets)/len(batch1_retweets)
	avg_sentiment = sum(batch1_sentiment)/len(batch1_sentiment)
	avg_diversity = sum(batch1_diversity)/len(batch1_diversity)
	out = "Avg Retweets\t{}\nAvg Sentiment\t{}\nAvg Diversity\t{}\n"
	print(out.format(avg_retweets,avg_sentiment,avg_diversity))

	print "Second Batch Statistics:"
	avg_retweets = sum(batch2_retweets)/len(batch2_retweets)
	avg_sentiment = sum(batch2_sentiment)/len(batch2_sentiment)
	avg_diversity = sum(batch2_diversity)/len(batch2_diversity)
	out = "Avg Retweets\t{}\nAvg Sentiment\t{}\nAvg Diversity\t{}\n"
	print(out.format(avg_retweets,avg_sentiment,avg_diversity))

	return

#=FACEBOOK MINING FUNCTIONS===============================================

#connFacebook - Returns Facebook connection
def connFacebook(fbOA_TOKEN,fbOA_SECRET,fbCONSUMER_KEY,fbCONSUMER_SECRET):
	fbConn = 0
	return fbConn

#mineFacebook - Performs batch mining and analysis
def mineFacebook(fbConn,fbPage,fbCount):
	return

#=WEBSITE MINING FUNCTIONS===============================================

#mineWebsite - Retrieves page HTML and performs page analysis
def mineWebsite(url,depth):

	#Retrieve HTML and Setup Russell
	html = requests.get(url)
	fileObj = codecs.open("russel.rtf","w","UTF")
	print "Latest News Article: " + str(url)

	#Build DOM and List Paragraphs
	soup = BeautifulSoup(html.text,'html5lib')
	paras = soup.find_all('p')

	#Parse HTML Paragraphs
	unicode_text = ""
	for para in paras:
		fileObj.write(para.text)
		unicode_text = unicode_text + para.text

	#Summarize Paragraph Text
	summary = Russell.summarize(unicode_text)
	print "\nThree Sentence Article Summary:"
	for sent in summary['top_n_summary']:
		print removeUnicode(sent)

	#Tokenize Paragraph Text and Remove Stop Words
	ascii_text = removeUnicode(unicode_text)
	tokens = nltk.tokenize.word_tokenize(ascii_text)
	wordlist = []
	for word in tokens:
		word = word.lower()
		if word not in STOPWORDS:
			wordlist.append(word)

	#Collect Collocations and Filter
	collocs = nltk.BigramCollocationFinder.from_words(wordlist)
	collocs.apply_freq_filter(2)
	collocs.apply_word_filter(lambda skips: skips in nltk.corpus.stopwords.words('English'))

	#Parse Collocs for Bigrams
	jaccard = BigramAssocMeasures.jaccard
	bigrams = collocs.nbest(jaccard,10)

	#Summarize Bigrams
	print "\nArticle Bigram List:"
	for bigram in bigrams:
		print str(bigram[0]).encode('utf-8')," ",str(bigram[1]).encode('utf-8')
	
	return

#=MAIN==================================================================

def main():

	#Twitter Access Credential Declaration
	twOA_TOKEN = ''
	twOA_SECRET = ''
	twCONSUMER_KEY = ''
	twCONSUMER_SECRET = ''

	#Facebook Access Credential Declaration
	fbOA_TOKEN = ''
	fbOA_SECRET = ''
	fbCONSUMER_KEY = ''
	fbCONSUMER_SECRET = ''

	#Mining Targets Declaration
	twAt = "@spacex"
	twCount = 25
	fbPage = ""
	fbCount = 0
	url = "http://www.spacex.com/news/2017/03/16/echostar-xxiii-mission"
	depth = 0

	#Establish Connection to Twitter and Mine
	twConn = connTwitter(twOA_TOKEN,twOA_SECRET,twCONSUMER_KEY,twCONSUMER_SECRET)
	mineTwitter(twConn,twAt,twCount)

	#Establish Connection to Facebook and Mine
	fbConn = connFacebook(fbOA_TOKEN,fbOA_SECRET,fbCONSUMER_KEY,fbCONSUMER_SECRET)
	mineFacebook(fbConn,fbPage,fbCount)

	#Retrieve Webpage HTML and Parse
	mineWebsite(url,depth)

main()
