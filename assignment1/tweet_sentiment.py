import sys
import json


def assumptions(word_sentiment):
    """Double-check some assumptions I've made. """

    for key in word_sentiment:
        if (key.lower() != key):
            raise "Case-sensitive key: '" + key + "'"

        if (' '.join(key.split(' ')) != key):
            raise "Multiple whitespaces in key: '" + key + "'"
    
def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiment = {key: int(value) for (key, value) in map(lambda x: x.split("\t"), sent_file.readlines())}
    assumptions(sentiment)
    # Make key into tuple for easier checking of phrases.
    sentiment = {tuple(key.split(' ')): value for (key, value) in sentiment.items()}

    tweet_texts = [tweet['text'] for tweet in map(json.loads, tweet_file.readlines()) if tweet.has_key('text')]
    tweet_texts = map(lambda x: x.replace("\n", "\\n"), tweet_texts)

    max_phrase_size = reduce(max, map(len, sentiment.keys()))

    for tweet in tweet_texts:

        ts = 0.0
        matches = []
        
        words = tweet.split(' ')

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

        #print "%s:%f:%s" % (tweet,ts, matches)
        print "%f" % (ts)        

if __name__ == '__main__':
    main()
