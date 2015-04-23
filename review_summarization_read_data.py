import os
import nltk
import json

all_destinations = os.listdir("Training_data")

reviews_per_destination = {}
destinations_per_id = {}
destination_id = 0

# Read Data
for destination in all_destinations :
	
	with open("Training_data/"+destination) as current_destination :
		
		data = current_destination.read().replace('\n', '').split('********************')
		
		reviews = data[2:]
		
		reviews_per_destination[destination_id] = reviews
	
	destinations_per_id[destination_id] = destination.split('.')[0]
	
	destination_id += 1	

reviews_json = open("reviews_per_destination.json", "w")
destinations = open("all_destinations.json", "w")

json.dump(reviews_per_destination, reviews_json)
json.dump(destinations_per_id, destinations);

reviews_json.close()
destinations.close()
