import facebook
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

def getDiversity(text):
  words = text.split()
  return 1.0 * len(set(words))/len(words)

def getSentiment(text):
  vs = vaderSentiment(text.encode("utf-8"))
  return vs["compound"]

def removeUnicode(text):
    asciiText = ""
    for char in text:
        if(ord(char) < 128):
            asciiText = asciiText + char
    return asciiText

def postAnalyze(post, num):
	text = removeUnicode(post["message"])
	#likes = ???
	sentiment = getSentiment(text)
	diversity = getDiversity(text)
	out = "Post {}:\nText:\t{}\nSentiment: {}, Lexical diversity: {}\n"
	print(out.format(num, text, sentiment, diversity))
	return sentiment, diversity


def mineFacebook(token, fbPage, fbCount):
    fb = facebook.GraphAPI(token)
    d_posts = fb.get_connections(fbPage, 'posts')
    
    total_sentiment = []
    total_diversity = []
    
    posts = 0
    for i in range(25):
        curPost = d_posts['data'][i]
        if curPost['type'] != 'video':
            posts = posts + 1
            sentiment, diversity = postAnalyze(curPost, posts)
            
            total_sentiment.append(sentiment)
            total_diversity.append(diversity)
            
            if posts == fbCount:
                break
            
    avg_sentiment = sum(total_sentiment)/len(total_sentiment)
    avg_diversity = sum(total_diversity)/len(total_diversity)
    out = "Avg Sentiment\t{}\nAvg Diversity\t{}\n"
    print(out.format(avg_sentiment,avg_diversity))
    
    return

def main():
    token = "EAACEdEose0cBAHqQZBWFIYKuMmKfZC3ZC7Ai393mVaj8vyXDSg53EFZCmKn2uGMbr3P1JpRcsRyYcZBGpvYqyyC2dawXh2eFPc5c96qQCR9n3vwOA5j5lqzyCHbrfZAmu0xMT3bnZCgh5MiAaPYJAw3ilFb4zzVKrDneoFM3b2FWbUWZAEXY5m4ZCTet9cWKqZAeAZD"
    fbPage = "NASA"
    fbCount = 10
    
    mineFacebook(token, fbPage, fbCount)
    
    
main()