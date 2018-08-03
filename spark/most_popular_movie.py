import re
from pyspark import SparkContext, SparkConf


def load_movie_names():
    movie_names = {}
    with open("ml-100k/u.item", encoding="ISO-8859-1") as f:
        for line in f:
            fields = line.split("|")
            movie_names[fields[0]] = fields[1]
    return movie_names


if __name__ == "__main__":
    conf = SparkConf().setMaster("local").setAppName("RatingsHisto")
    sc = SparkContext(conf=conf)

    name_dict = sc.broadcast(load_movie_names())

    lines = sc.textFile("ml-100k/u.data")
    movies = lines.map(lambda x: (x.split()[1], 1))
    movie_counts = movies.reduceByKey(lambda x, y: x + y).map(
        lambda x: (x[1], x[0])).sortByKey(ascending=False)

    movie_counts_with_names = movie_counts.map(
        lambda x: (name_dict.value[x[1]], x[0]))
    for movie in movie_counts_with_names.collect():
        print(f"{movie[0]}: {movie[1]}")