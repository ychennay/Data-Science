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
    wordCount = tokens.map(lambda x: (x, 1)).reduceByKey(
        lambda x, y: x + y).map(lambda x: (x[1],x[0])).sortByKey(ascending=False)

    results = wordCount.collect()
    for result in results: print(f"{result[0]}: {result[1]}")