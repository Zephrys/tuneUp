import math
from neo4jrestclient.client import GraphDatabase
from pprint import pprint
import sys

MOVIE_COUNT = 3883
USER_COUNT = 6040

graph = GraphDatabase("http://172.17.30.135:7474/db/data/", username="neo4j", password="admin")
user_average = {}
related_users = {}
nodes = {}
bad_nodes = {}


# solve cold start
def add_base_line():
    query = """MATCH (u:User)-[r:RATED]->(m:Movie) RETURN u.name, m.name"""
    rating_av = """MATCH (u:User)-[r:RATED]->(m:Movie) RETURN avg(r.score)"""
    rating_av = graph.query(rating_av, data_contents=True).rows[0][0]
    result = graph.query(query, data_contents=True).rows
    movies = graph.labels.get('Movie')
    users = graph.labels.get('User')
    for u in xrange(1, USER_COUNT+1):
        for m in xrange(1, MOVIE_COUNT+1):
            if [u,m] in result:
                continue
            else:
                query = """MATCH (u:User)-[r:RATED]->(m:Movie) where u.name="%s" return avg(r.score)""" %(u)
                user_av = graph.query(query, data_contents=True).rows[0][0]
                query = """MATCH (u:User)-[r:RATED]->(m:Movie) where m.name="%s" return avg(r.score)""" %(m)
                movie_av = graph.query(query, data_contents=True).rows[0][0]
                baseline = float(user_av) + float(movie_av) - float(rating_av)
                user = users.get(name=str(u))
                movie = movies.get(name=str(m))
                user.relationships.create("RATED", movie, score=baseline)

def get_nodes():
    movies = graph.labels.get('Movie')
    for i in xrange(1, MOVIE_COUNT+1):
        nodes[i] = movies.get(name=str(i))
        if len(nodes[i]) !=0:
            nodes[i] = nodes[i][0]
            bad_nodes[i] = False
        else:
            bad_nodes[i] = True

def get_user_average():
    for i in xrange(1, USER_COUNT+1):
        query = """MATCH (u:User)-[r:RATED]->(m:Movie) WHERE u.name="%s" RETURN avg(r.score)""" % (i)
        result = graph.query(query, data_contents=True)
        user_average[str(i)] = result.rows[0][0]


def get_related_users():
    for i in xrange(1, MOVIE_COUNT +1):
        query = """MATCH (u:User)-[r:RATED]->(m:Movie) WHERE m.name='%d'  RETURN u.name, r.score""" % i
        result = graph.query(query, data_contents=True)
        if len(result) != 0:
            result = {x[0]:x[1] for x in result.rows}
        else:
            result = {}
        related_users[i] = result


def score(i, j):
    # dictionary that maps user to score
    movie_i = related_users[i]
    #check for zero and break

    if len(movie_i) == 0:
        return 0

    movie_j = related_users[j]

    intersection = set(movie_i.keys()).intersection(movie_j.keys())

    score = 0.0
    denominator_i = 0.0
    numerator = 0.0
    denominator_j = 0.0

    for user in intersection:
        numerator = numerator + (movie_i[user] - user_average[user])*(movie_j[user] - user_average[user])
        denominator_i = denominator_i + (movie_i[user] - user_average[user])*(movie_i[user] - user_average[user])
        denominator_j = denominator_j + (movie_j[user] - user_average[user])*(movie_j[user] - user_average[user])

    if denominator_i == 0 or denominator_j == 0:
        return 0
    return numerator/(math.sqrt(denominator_i*denominator_j))


def main():

    print "%s %s" % (sys.argv[1], sys.argv[2])
    print "This program goes through the graph and finds the similarity between given items"
    get_nodes()
    print "Nodes Processed"
    get_user_average()
    print "Averages Processed"
    get_related_users()
    print "Related users pre processed"

    for i in xrange(int(sys.argv[1]), int(sys.argv[2])):
        print i
        if bad_nodes[i]:
            continue
        for j in xrange(i + 1, MOVIE_COUNT + 1):
            if bad_nodes[i]:
                continue
            similarity = score(i, j)
            if similarity != 0:
                nodes[i].relationships.create("SIMILARITY", nodes[j], score=similarity)

if __name__ == "__main__":
    add_base_line()
    main()
