import sys
import operator
import json
    
def main():
    tweet_file = open(sys.argv[1])

    frequencies = {}
    count = 0

    def update(map, text):
        for term in text.split():
            map[term] = map.get(term, 0) + 1
        return map

    tweets = filter(lambda x: x.has_key('text'),
                    map(json.loads, tweet_file.readlines()))

#    for tweet in tweets:
#        terms = tweet['text'].split()
#        for term in terms:
#            print term


    frequencies = reduce(update,
                         map(lambda x: x['text'], tweets),
                         {})
    total = reduce(operator.add, frequencies.values())

    for term in frequencies:
        print "%s %f" % (term, float(frequencies[term])/total)


if __name__ == '__main__':
    main()
