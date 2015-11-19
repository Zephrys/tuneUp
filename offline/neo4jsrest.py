import math
from neo4jrestclient.client import GraphDatabase

MOVIE_COUNT = 30106
USER_COUNT = 234934


def main():

	graph = GraphDatabase("http://localhost:7474/db/data/", username="neo4j", password="admin")
	ratings = open('../data/ratings.csv', 'r')
	movies = graph.labels.create("Movies")
	users = graph.labels.create("Users")

	next(ratings)
	for rating in ratings:
		rating = rating.split(",")
		user = users.get(name=str(rating[0]))
		if not user:
			user = graph.nodes.create(name=str(rating[0]))
			users.add(user)
		else:
			user = user[0]

		movie = movies.get(name=str(rating[1]))
		if not movie:
			movie = graph.nodes.create(name=str(rating[1]))
			movies.add(movie)
		else:
			movie = movie[0]

		user.relationships.create("Rated", movie, rate=float(rating[2]))

	print "Graph Created"

if __name__ == "__main__":
	main()