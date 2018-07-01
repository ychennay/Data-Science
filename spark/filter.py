from pyspark import SparkContext, SparkConf


def parse_record(line):
    tokens = line.split(",")
    year = tokens[1]
    data_type = tokens[2]
    temperature = float(tokens[3])
    return (data_type, year, temperature)


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("filter")
    sc = SparkContext(conf=conf)
    lines = sc.textFile("1800.csv")
    parsed_lines = lines.map(parse_record)
    min_lines = parsed_lines.filter(lambda x: x[0] == "TMIN").map(
        lambda x: (x[1], x[2]))
    max_lines = parsed_lines.filter(lambda x: x[0] == "TMAX").map(
        lambda x: (x[1], x[2]))
    min_temps = min_lines.reduceByKey(lambda x, y: min(x, y))
    max_temps = max_lines.reduceByKey(lambda x, y: max(x, y))
    print(min_temps.collect())
    print(max_temps.collect())