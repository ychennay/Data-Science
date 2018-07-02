from pyspark import SparkContext, SparkConf
from math import sqrt


def loadMovieNames():
    movieNames = {}
    with open('ml-1m/movies.dat', encoding="ISO-8859-1") as f:
        for line in f:
            fields = line.split("::")
            movieNames[fields[0]] = fields[1]
    return movieNames


def filter_duplicates(entry):
    user_rating_pair = entry[1]
    rating1 = user_rating_pair[0]
    rating2 = user_rating_pair[1]
    movie_id1 = rating1[0]
    movie_id2 = rating2[0]
    return movie_id1 < movie_id2


def make_pairs(entry):
    ratings = entry[1]
    movie1, rating1 = ratings[0]
    movie2, rating2 = ratings[1]
    return (movie1, movie2), (rating1, rating2)


def compute_cosine_similarity(pairs):
    num_pairs = 0
    sum_xx = sum_yy = sum_xy = 0
    for ratingX, ratingY in pairs:
        sum_xx += ratingX * ratingX
        sum_yy += ratingY * ratingY
        sum_xy += ratingX * ratingY
        num_pairs += 1

    numerator = sum_xy
    denominator = sqrt(sum_xx) * sqrt(sum_yy)
    score = 0
    if denominator:
        score = numerator / float(denominator)
    return score, num_pairs


if __name__ == "__main__":
    MOVIE_ID = '50'
    THRESHOLD = .97
    CO_OCCURENCE = 50
    conf = SparkConf()
    sc = SparkContext(conf=conf)

    nameDict = loadMovieNames()
    data = sc.textFile("s3n://sundog-spark/ml-1m/ratings.dat")
    mapped_data = data.map(lambda x: x.split("::")).map(lambda x: (x[0], (x[1], float(x[2]))))
    unique_joined_data = mapped_data.join(mapped_data).filter(filter_duplicates)
    movie_pairs = unique_joined_data.map(make_pairs)

    movie_pairs_ratings = movie_pairs.groupByKey()
    similarities = movie_pairs_ratings.mapValues(compute_cosine_similarity).cache()
    relevants = similarities.filter(lambda sim: sim[0][0] == MOVIE_ID or sim[0][1] == MOVIE_ID)
    good_matches = relevants.filter(lambda sim: sim[1][0] > THRESHOLD and sim[1][1] > CO_OCCURENCE)
    best_matches = good_matches.map(lambda x: (x[1], x[0])).sortByKey(ascending=False).take(10)

    print(f"Top 10 films for {nameDict[MOVIE_ID]}")
    for match in best_matches:
        sim, pair = match
        similar_movie_id = pair[0]
        if similar_movie_id == MOVIE_ID:
            similar_movie_id = pair[1]
        print(f"{nameDict[similar_movie_id]} score: {sim[0]}, strength: {sim[1]}")