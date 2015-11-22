import sys
from time import sleep

def main():
	ndata = {}
	print "Loading csv now!"
	csvfile = open('../data/similarity.csv')

	line = csvfile.readline()
	line = csvfile.readline()

	line_list = line.split(',')
	print line_list

	start_id = int(line_list[0])
	curr_id = start_id
	curr_num = 1

	answer_dict = {}

	rank_dict = {}
	#  the string property of similarity (float actually) is preserved! :D
	rank_dict[line_list[2]] = int(line_list[1])

	print rank_dict

	# sys.exit(0)
	
	for i, line in enumerate(csvfile):
		# if i == 4000:
		# 	break
		# else:
		# 	print i

		print i
		
		line_list = line.split(',')

		curr_id = int(line_list[0])

		if curr_id == start_id:
			rank_dict[line_list[2]] = int(line_list[1])
		else:
			# Probably a bunch of explaination required here!
			sorted_keys = sorted(rank_dict.keys())
			ans = {}
			# sleep(1)
			print "now printing X"
			# print sorted_keys
			for x in xrange(1, 11):
				print x
				try:
					ans[str(x)] = (sorted_keys[x], rank_dict[sorted_keys[x]])
				except IndexError:
					break;

			answer_dict[str(start_id)] = ans

			start_id = curr_id
			
			rank_dict = {}

	print " I am now writing into our answer file, from where we'll fetch stuff! :)"
	writefile = open('output.py', 'w')
	writefile.write("reco = ")
	writefile.write(str(answer_dict))

if __name__ == '__main__':
	main()