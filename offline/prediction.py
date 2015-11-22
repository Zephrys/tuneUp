# 
# Prediction.py 
#

import neo4jrestclient
import pandas as pd
import numpy as np
from neo4jrestclient.client import GraphDatabase
import sys
from time import sleep
from prettytable import PrettyTable

print "Pandas loaded"

graph = GraphDatabase("http://172.17.30.135:7474/db/data/", username="neo4j", password="admin")

print "Loading Similarity CSV now"

csv = pd.read_csv('../data/similarity.csv', index_col=0)

print "CSV Lookups!"

a = [0]*3884

for smov_id in xrange(1, 3884):
    try:
        if smov_id % 500 == 0:
            print smov_id, "now"
        
        a[smov_id] = csv.lookup([smov_id, smov_id], ["similar", "score"])
    except KeyError:
        a[smov_id] = 0
        continue

print "Loaded Everything"


def main():
    print "Welcome to MovieLens Recommender System"

    while True:
        user_id = raw_input("Enter the User ID corresponding to which you'd like predictions or press Q/q to quit\n> ")
        if user_id.lower() == 'q':
            sys.exit(0)


        query = """MATCH (u:User)-[r:RATED]->(m:Movie) WHERE u.name='%s'  RETURN m.name, r.score""" %user_id
        result = graph.query(query, data_contents=True) 
        movie_exists = {int(x[0]): float(str(x[1])) for x in result.rows}
        print sorted(movie_exists.keys())

        # print result.rows
        prediction = {}

        for movie_id in xrange(1, 3883 + 1):
            if movie_id in movie_exists.keys():
                continue
            else:
                smov_id = movie_id

                global a
                a1 = a[movie_id]

                if type(a1) == int:
                    continue
                else:
                    similar_score = [float(str(x)) for x in a1.tolist()[1].tolist()]
                    similar_id = a1.tolist()[0].tolist()

                    similar_dict = dict(zip(similar_id, similar_score))
                    
                    num = 0.0
                    deno = 0.0

                    for y in movie_exists.keys():
                        if similar_dict.get(y, False):
                            num += movie_exists[y] * float(str(similar_dict[y]))
                            deno += float(similar_dict[y])


                    if prediction.get(str(num/deno), False):
                        prediction[str(num/deno)] += [movie_id]
                    else:
                        prediction[str(num/deno)] = [movie_id]
        
        key_s = sorted(prediction.keys() , reverse = True)

        count = 0

        print "loading movies.csv now! "
        movies_csv = pd.read_csv('../data/movies.csv', index_col=0, names=["Id", "name", "genres"])



        table = PrettyTable(["Movie ID", "Movie Name", "Score"])

        for key in key_s:
            count = count + len(prediction[key])
            for movie in prediction[key][:10]:
                ans =  movies_csv.lookup([movie], ["name"]).tolist()
                table.add_row([movie, ans[0], key]) 
            if count >= 10:
                break


        print table


if __name__ == '__main__':
    main()