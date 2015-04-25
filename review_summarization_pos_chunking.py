import nltk
import json
import time

start = time.time()

reviews_per_destination = json.load(open("reviews_per_destination.json", "r"))
#destinations_per_id = json.load(open("all_destinations.json", "r"))

#POS Tagging
tagged_reviews_per_desination = {}

#Chunking
patterns = r"""NP: 
				{<DT|PP\$>?<JJ>*<NN>}
				{<NNP>+}
				{<NN>+}
			""" 	# define a tag pattern of an NP chunk

NPChunker = nltk.RegexpParser(patterns) 					# create a chunk parser

for destination_id in reviews_per_destination :
	
	pos_tagged_reviews = []

	reviews = reviews_per_destination[destination_id]

	for review in reviews:
		review_tokenised = nltk.word_tokenize(review)
		review_pos_tagged = nltk.pos_tag(review_tokenised)
		
		review_chunked = NPChunker.parse(review_pos_tagged)
		'''
		i = 0
		while i < len(review_pos_tagged) :
			review_pos_tagged[i] = "/".join(review_pos_tagged[i])
			i += 1
		'''	
		pos_tagged_reviews.append(review_chunked)

	tagged_reviews_per_desination[destination_id] = pos_tagged_reviews

json.dump(tagged_reviews_per_desination, open("tagged_reviews_per_destination.json", "w"))

end = time.time()

print(end-start)
