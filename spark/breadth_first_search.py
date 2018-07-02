from pyspark import SparkContext, SparkConf


def create_bfs(line):
    fields = line.split()
    heroID = str(fields[0])
    connections = []
    for connection in fields[1:]:
        connections.append(str(connection))

    color = 'WHITE'
    distance = 9999

    if heroID == starting_hero_id:
        color = 'GRAY'
        distance = 0

    return heroID, (connections, distance, color)


def create_starting_rdd():
    return sc.textFile("Marvel-Graph.txt").map(create_bfs)


def map_bfs(node):
    characterID = node[0]
    data = node[1]
    connections = data[0]
    distance = data[1]
    color = data[2]

    results = []

    #If this node needs to be expanded...
    if (color == 'GRAY'):
        print(f"Character id {characterID} is gray.")
        for connection in connections:
            newCharacterID = connection
            newDistance = distance + 1
            newColor = 'GRAY'
            if (target_hero_id == connection):
                hit_counter.add(1)

            newEntry = (newCharacterID, ([], newDistance, newColor))
            results.append(newEntry)

        #We've processed this node, so color it black
        color = 'BLACK'

    #Emit the input node so we don't lose it.
    results.append( (characterID, (connections, distance, color)) )
    # print(f"length of result is {len(results)}")
    return results


def bfs_reduce(data1, data2):
    edges1 = data1[0]
    edges2 = data2[0]
    distance1 = data1[1]
    distance2 = data2[1]
    color1 = data1[2]
    color2 = data2[2]

    distance = 9999
    color = color1
    edges = []

    if len(edges1) > 0:
        edges.extend(edges1)
    if len(edges2) > 0:
        edges.extend(edges2)

    # Preserve minimum distance
    if distance1 < distance:
        distance = distance1

    if distance2 < distance:
        distance = distance2

    if color1 == 'WHITE' and (color2 == 'GRAY' or color2 == 'BLACK'):
        color = color2

    if color1 == 'GRAY' and color2 == 'BLACK':
        color = color2

    if color2 == 'WHITE' and (color1 == 'GRAY' or color1 == 'BLACK'):
        color = color1

    if color2 == 'GRAY' and color1 == 'BLACK':
        color = color1

    return edges, distance, color


if __name__ == "__main__":

    starting_hero_id = '5306'  # Spiderman
    target_hero_id = '14'  # a superhero named ADAM

    conf = SparkConf().setMaster("local").setAppName("BFS")
    sc = SparkContext(conf=conf)
    hit_counter = sc.accumulator(0)

    bfs_rdd = create_starting_rdd()

    for iteration in range(10):
        print(f"Running BFS iteration #{iteration}.")

        mapped = bfs_rdd.flatMap(map_bfs)
        print(f"Processed {mapped.count()} values")

        if hit_counter.value > 0:
            print(f"We found the connection between "
                  f"{starting_hero_id}  and {target_hero_id}, from {hit_counter} different paths.")
            break

        bfs_rdd = mapped.reduceByKey(bfs_reduce)