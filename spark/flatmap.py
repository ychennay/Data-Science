import re
from pyspark import SparkContext, SparkConf
from collections import OrderedDict


def clean_words(words):
    return re.compile(r'[\d\W]+', re.UNICODE).split(words.lower())

if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("RatingsHisto")
    sc = SparkContext(conf=conf)

    book = sc.textFile("Book.txt")
    tokens = book.flatMap(clean_words)
    wordCount = tokens.countByValue()
    results = OrderedDict(sorted(wordCount.items()))
    for word, count in results.items():
        cleanWord = word.encode("ascii", 'ignore')
        if cleanWord:
            print(f"{cleanWord}: {count}")