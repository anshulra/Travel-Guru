import nltk
import json
import time

start = time.time()

chunked_reviews_per_destination = json.load(open("chunked_reviews_per_destination.json", "r"))

# A list of review sentences for each opinioned feature 
sentences_per_feature_per_destination = {}

# A count of opinion words in each sentence per destination
#sentence_orientation_per_destination = {}

# Stopwords in english
stopwords = nltk.corpus.stopwords.words('english')

# Given a feature (i.e. a NP) this function removes stopwords. It then checks if the feature is a unigram
def feature_pruning(feature) :
	for word,tag in feature :
		if bool(2 <= len(word) <= 40) == False or (word in stopwords) :
			feature.remove((word,tag))
	
	if len(feature) > 1 :
		return feature
	else :
		return False

# An adjective is considered to be an "opinion word". Given a feature (i.e. a NP) this function counts the number of opinion words in it
def opinion_word_detection(feature) :
	for word,tag in feature :
		if tag == 'JJ' :
			#opinion_word_count += 1
			return True
			
	#return opinion_word_count
	return False
	
# Given a chunked review sentence, this function traverses the tree. If a Noun Phrase is found, it is considered a "feature" of this review. This function then performs pruning and opinion_word_detection on this feature
def traverse(review, review_index, destination_id) :
	
	global opinion_words
	try:
		review.label()
	except AttributeError:
		return
	
	if review.label() == 'NP': 
		
		feature = feature_pruning(list(review))
		if feature == False :
			return
		
		if opinion_word_detection(feature) == False :
			return
		
		# Add review index to occurence
		for word,tag in feature :
			if tag == 'NN' :
				if word not in sentences_per_feature_per_destination[destination_id] :
					sentences_per_feature_per_destination[destination_id][word] = []
			
				sentences_per_feature_per_destination[destination_id][word].append(review_index)

	else:
		for child in review:
			traverse(child, review_index, destination_id)


# For each review sentence per destination find the opinion keywords in the sentence
for destination_id in chunked_reviews_per_destination :
	
	chunked_reviews = chunked_reviews_per_destination[destination_id]
	
	sentences_per_feature_per_destination[destination_id] = {}
	
	for review_index in chunked_reviews :
		
		traverse(chunked_reviews[review_index], review_index, destination_id)

json.dump(sentences_per_feature_per_destination, open("sentences_per_feature_per_destination.json", "w"))
