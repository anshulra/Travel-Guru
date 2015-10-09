import nltk
import json

reviews_per_destination = json.load(open("reviews_per_destination.json", "r"))

#POS Tagging
chunked_reviews_per_destination = {}

#Chunking patterns to detect Noun Phrases
patterns = r"""
			NP:
				{<NN.*|JJ>*<NN.*>}
				{<NN.*|JJ>*<NN.*><IN><NN.*|JJ>*<NN.*>}  # Above, connected with in/of/etc...
			"""

NPChunker = nltk.RegexpParser(patterns) 					# create a chunk parser

# For each revview sentence in a destination perform POS tagging. Then perform chunking using nltk.
for destination_id in reviews_per_destination :
	
	chunked_reviews = {}

	reviews = reviews_per_destination[destination_id]

	for review_index in reviews:
		review_tokenised = nltk.word_tokenize(reviews[review_index].lower())
		review_pos_tagged = nltk.pos_tag(review_tokenised)
		
		review_chunked = NPChunker.parse(review_pos_tagged)

		chunked_reviews[review_index] = review_chunked
		
	chunked_reviews_per_destination[destination_id] = chunked_reviews
	
chunked_json = open("chunked_reviews_per_destination.json", "w")
json.dump(chunked_reviews_per_destination, chunked_json)
chunked_json.close()

