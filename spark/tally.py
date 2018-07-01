from pyspark import SparkConf, SparkContext

if __name__ == "__main__":

    conf = SparkConf().setMaster("local").setAppName("tally")
    sc = SparkContext(conf=conf)

    orders = sc.textFile("customer-orders.csv")
    tokens = orders.map(lambda x: x.split(",")).map(lambda x: (x[0], float(x[2])))
    results = tokens.reduceByKey(lambda x, y: x + y).map(lambda x: (x[1], x[0]))
    sums = results.sortByKey(ascending=False).map(lambda x: (x[1], x[0]))