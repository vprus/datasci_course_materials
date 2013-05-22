import sys
import operator
import json
    
def main():
    tweet_file = open(sys.argv[1])
    tweets = filter(lambda x: x.has_key('text'),
                    map(json.loads, tweet_file.readlines()))

    frequencies = {}
    count = 0

    def update(map, terms):
        for term in terms:
            map[term] = map.get(term, 0) + 1
        return map

    def hashtags(tweet):
        return map(lambda x: x['text'], tweet.get('entities', {}).get('hashtags', []))

    frequencies = reduce(update,
                         map(hashtags, tweets),
                         {})
    fl = [(term, count) for (term, count) in frequencies.items()]
    fl.sort(lambda a, b: b[1] - a[1])
    for (term, count) in fl[0:10]:
        print "%s %f" % (term, count)


if __name__ == '__main__':
    main()
