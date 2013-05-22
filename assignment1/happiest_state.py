import sys
import json

us_states = ["AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FM", "FL", "GA", "GU", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MH", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "MP", "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VI", "VA", "WA", "WV", "WI", "WY"]

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


    def state_from_location(location):
                split = location.split(',');
                if len(split) == 2:
                    state = split[1].strip()
                    if state in us_states:
                        return state


    def us_state(tweet):

        user = tweet.get('user', None)
        if user:
            location = user['location']
            if location:
                state = state_from_location(location)
                if state:
                    return state

        place = tweet.get('place', None)
        if place:
            location = place['full_name']
            if location:
                state = state_from_location(location)
                if state:
                    return state

    state_tweets = {}
    count = 0
    for tweet in tweets:
        state = us_state(tweet)
        if state:
            state_tweets.setdefault(state, []).append(tweet)
            count = count + 1

    #print "Tweets with state:", count

    state_happiness = [(state, average_sentiment(tweets)) for (state, tweets) in state_tweets.items()]
    state_happiness.sort(lambda a, b: cmp(b[1], a[1]))

    print state_happiness[0][0]

if __name__ == '__main__':
    main()
