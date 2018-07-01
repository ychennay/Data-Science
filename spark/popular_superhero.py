from pyspark import SparkContext, SparkConf


def parse_names(name):
    tokens = name.split('"')
    hero_id = str(tokens[0]).strip()
    hero_name = tokens[1].strip()
    return hero_id, hero_name


def count_cooccurences(line):
    tokens = line.split()
    return tokens[0], len(tokens) - 1


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("RatingsHisto")
    sc = SparkContext(conf=conf)
    names = sc.textFile("Marvel-Names.txt")
    names_rdd = names.map(parse_names).collect()

    lines = sc.textFile("Marvel-Graph.txt")
    pairings = lines.map(count_cooccurences)
    total_friends_by_character = pairings.reduceByKey(lambda x, y: x + y)
    print(total_friends_by_character.collect())
