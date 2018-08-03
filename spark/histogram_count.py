from collections import OrderedDict
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("RatingsHisto")
    sc = SparkContext(conf=conf)

    lines = sc.textFile("ml-100k/u.data")
    ratings = lines.map(lambda x: x.split()[2])
    result = ratings.countByValue()
    sorted_results = OrderedDict(sorted(result.items()))
    for rating, count in sorted_results.items():
        print(f"{rating}: {count}")