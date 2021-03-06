import csv
import re
from util import *

P = dict()
# (word, O/E score, O, E) 
word_tuples = []
word_tuples_by_length = []
total_char_count = 0
total_word_count = 0

# (l - k + 1) * P(w)
def get_expected(word):
	ret = total_char_count - len(word) + 1
	for letter in word:
		ret *= P[letter]
	return ret

def save_part1():
	header = ['word', 'O/E', 'obs', 'E']
	with open('output/part1_letter_probability.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['letter', 'P'])
		keys = P.keys()
		keys = sorted(keys)
		for key in keys:
			writer.writerow([key, P[key]])
	with open('output/part1_result_full.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerows(word_tuples)
	with open('output/part1_result_top_bott_50OE.csv', 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(['top 50'])
		writer.writerow(header)
		writer.writerows(word_tuples[1:51])
		writer.writerow(['bottom 50'])
		writer.writerow(header)
		writer.writerows(word_tuples[-51:-1])
	with open('output/part1_result_top_bott_50OE_by_length.csv', 'wb') as f:
		writer = csv.writer(f)
		for tuples in word_tuples_by_length:
			if not tuples: continue
			writer.writerow(['word length ' + str(len(tuples[0][0]))])
			writer.writerow(['top 50 O/E'])
			writer.writerow(header)
			writer.writerows(tuples[1:51])
			writer.writerow(['bottom 50 O/E'])
			writer.writerow(header)
			writer.writerows(tuples[-51:-1])
			writer.writerow([])
	with open('output/part1_result_top_bott_50O_by_length.csv', 'wb') as f:
		writer = csv.writer(f)
		for tuples in word_tuples_by_length:
			if not tuples: continue
			temp = sorted(tuples, key = lambda obs : obs[2], reverse = True)
			writer.writerow(['word length ' + str(len(temp[0][0]))])
			writer.writerow(['top 50 Observation'])
			writer.writerow(header)
			writer.writerows(temp[:51])
			writer.writerow(['bottom 50 Observation'])
			writer.writerow(header)
			writer.writerows(temp[-51:])
			writer.writerow([])

if __name__ == '__main__':
	file_name = 'complete_book_of_cheese_nows'
	total_char_count, P = load_probability_table('letter_occurrence/'+file_name)
	test_probability_table(P)

	with open('word_occurrence/'+file_name, 'r') as file:
		_ = file.readline()
		for line in file:
			tokens = re.split('[\t| ]+', line)
			E = get_expected(tokens[0])
			word_tuples.append((tokens[0], float(tokens[1])/E, int(tokens[1]), E))

	for i in xrange(11):
		word_tuples_by_length.append([])
	for elem in word_tuples:
		word_tuples_by_length[len(elem[0]) - len(word_tuples[0][0]) + 1].append(elem)


	for i in xrange(len(word_tuples_by_length)):
		word_tuples_by_length[i] = sorted(word_tuples_by_length[i], \
			key = lambda word : word[1], reverse = True)

	word_tuples = sorted(word_tuples, key = lambda word : word[1], reverse = True)

	save_part1()
