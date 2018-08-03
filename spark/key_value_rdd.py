from pyspark import SparkContext, SparkConf


def parse_line(line):
    tokens = line.split(",")
    age = tokens[2]
    friends = int(tokens[3])
    return (age, friends)


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("key_value")
    sc = SparkContext(conf=conf)
    lines = sc.textFile("fakefriends.csv")
    age_friends = lines.map(parse_line)
    counts = age_friends.mapValues(lambda x: (x, 1))
    totals = counts.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
    averages = totals.mapValues(lambda x: x[0] / x[1])
    results = averages.collect()
    [print(result) for result in results]