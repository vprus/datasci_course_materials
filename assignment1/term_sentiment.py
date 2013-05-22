import sys
import json

def assumptions(word_sentiment):
    """Double-check some assumptions I've made. """

    for key in word_sentiment:
        if (key.lower() != key):
            raise "Case-sensitive key: '" + key + "'"

        if (' '.join(key.split(' ')) != key):
            raise "Multiple whitespaces in key: '" + key + "'"

sentiment = {}
max_phrase_size = 0

def tweet_sentiment(tweet):

    ts = 0.0
    matches = []
    
    words = tweet['text'].split(' ')
    
    size = max_phrase_size
    while size > 0:
        
        i = 0
        while i+size < len(words):
            
            sub = words[i:i+size]
            
            key = tuple(sub)
            if sentiment.has_key(key):
                ts += sentiment[key]
                # Exclude this phrase from further
                # processing
                matches.append(key)
                del words[i:i+size]
            else:
                i = i + 1;
                
        size = size - 1

    return ts

def average_sentiment(tweets):
    
    return float(sum(map(tweet_sentiment, tweets))) / len(tweets)
        
def main():
    global sentiment
    global max_phrase_size
    
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiment = {key: int(value) for (key, value) in map(lambda x: x.split("\t"), sent_file.readlines())}
    assumptions(sentiment)
    # Make key into tuple for easier checking of phrases.
    sentiment = {tuple(key.split(' ')): value for (key, value) in sentiment.items()}

    tweets = [tweet for tweet in map(json.loads, tweet_file.readlines()) if tweet.has_key('text')]
    for tweet in tweets:
        tweet['text'] = tweet['text'].replace("\n", "\\n")

    max_phrase_size = reduce(max, map(len, sentiment.keys()))

    term_sentiments = {}
    for tweet in tweets:
        s = tweet_sentiment(tweet)      
        terms = tweet['text'].split()
        for term in terms:            
            term_sentiments.setdefault(term, []).append(s)

    for key in term_sentiments:
        term_sentiments[key] = float(sum(term_sentiments[key]))/len(term_sentiments[key])



#    context_sentiments = {}

    # For every term with known sentiment, collect context sentiments
#    for known in sentiment:
#        s = sentiment[known]
#        if len(known) != 1:
#            pass
#        known = known[0]
#        if term_sentiments.has_key(known):
#            context = term_sentiments[known]
#            context_sentiments.setdefault(s, []).append(context)
#
#    for key in context_sentiments:
#        context_sentiments[key] = float(sum(context_sentiments[key]))/len(context_sentiments[key])

#    for skey in sentiment:
#        if len(skey) == 1:
#            word = skey[0]
#            if word in term_sentiments:
#                print word, sentiment[skey], term_sentiments[word]

    for (key, value) in term_sentiments.items():
        print "%s %f" % (key, value)
    


#    report = term_sentiments.items()[:]
#    report = filter(lambda x: abs(x[1]) > 0.1, report)
#    report.sort(lambda a, b: cmp(a[1], b[1]))

#    for (term, context) in report:
#        print term, context

    
        

    
    
    
        


if __name__ == '__main__':
    main()
