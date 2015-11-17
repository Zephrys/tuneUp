import tables
import math

MOVIE_COUNT = 30106


def main():

	h5f = tables.open_file('database_name.h5', 'w')

	description_name = {}
	for movie in xrange(1,MOVIE_COUNT+1):
		description_name[str(movie)] = tables.Float32Col(dflt=0)
	description_name['average'] = tables.Float32Col(dflt=0)
	description_name['userid'] = tables.Float32Col()
	tb1 = h5f.create_table('/', 'useritemmatrix', description_name)

	fname = open('../data/ratings.csv', 'r')
	past = 1
	tot = 0.0
	count = 0
	for line in fname:
		data = line.split()
		if data[0] = past:
			tb1.row[str(data[1])] = float(data[2])
			tot = tot + float(data[2])
			count = count + 1
		else:
			tb1.row['average'] = tot/count
			tb1.row['userid'] = past
			past = data[0]
			tb1.row.append()
			tb1.row[str(data[1])] = float(data[2])

	description_name = {}
	for movie in xrange(1,MOVIE_COUNT+1):
		description_name[str(movie)] = tables.Float32Col(dflt=0)
	description_name['movieid'] = tables.Float32Col(dflt=0)
	tb2 = h5f.create_table('/', 'simmatix', description_name)
	# doesn't exploit sim(i,j) == sim(j,i)
	# @ToDO: exploit it
	# seems like i don't need movie id
	for movie_i in xrange(1, MOVIE_COUNT + 1):
		for movie_j in xrange(1, MOVIE_COUNT+1):
			num  = 0
			denom1 = 0
			denom2 = 0
			for row in tb1:
				if row[str(movie_i)] !=0 and row[str(movie_j)]!=0:
					num = num + (row[str(movie_i)] - row['average'])(row[str(movie_j)] - row['average'])
					denom1 = denom1 + (row[str(movie_i)] - row['average'])**2
					denom2 = denom2 + (row[str(movie_j)] - row['average'])**2
			tb1.row[str('movie_j')] = num/((math.sqrt(denom1))*math.sqrt(denom1))

if __name__ == "__main__":
	main()