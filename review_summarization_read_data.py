import os
import nltk
import json
import time

start = time.time()

all_destinations = os.listdir("Training_data")

# Review sentences for each destination
reviews_per_destination = {}

# All destinations in training data
destinations_per_id = {}
destination_id = 0

# Read Data
for destination in all_destinations :
	
	tokensized_reviews = {}
	review_index = 1
	
	# Read reviews for each destination
	with open("Training_data/"+destination, encoding='utf-8', errors='ignore') as current_destination :
		
		data = current_destination.read().replace('\n', ' ')
		data = data.replace('\\u00a0', '')
		# Tokenize review
		sentences = nltk.sent_tokenize(data)
			
		for sentence in sentences :
			tokensized_reviews[review_index] = sentence
			review_index += 1
	
		reviews_per_destination[destination_id] = tokensized_reviews
	
	destinations_per_id[destination_id] = destination.split('.')[0]
	
	destination_id += 1	
	
	if destination_id % 20 == 0 :
		print(destination_id)
	
review_json = open("reviews_per_destination.json", "w")
destinations_json = open("all_destinations.json", "w")

json.dump(reviews_per_destination, review_json)
json.dump(destinations_per_id, destinations_json);

review_json.close()
destinations_json.close()

end = time.time()
print(end-start)
