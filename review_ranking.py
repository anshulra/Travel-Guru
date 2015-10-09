import json
import re
queries = []

query_clusters = {}

sentences_per_feature_per_destination = json.load(open("sentences_per_feature_per_destination.json", "r"))
destinations_per_id = json.load(open("all_destinations.json", "r"))
reviews_per_destination = json.load(open("reviews_per_destination.json", "r", decoding='utf-8', errors="ignore"))

reviews_per_query_per_destination = {}

# Given a query and destination it ranks user reviews according to its coverage of the query
def review_ranking( queries , query_clusters, destination) :
	
	for i,d in destinations_per_id :
		if d == destination :
			destination_id = i
			break
	
	reviews_per_query_per_destination[destination_id] = {}
		
	for query in queries :
		
		reviews_per_query_per_destination[destination_id][query] = {} 
		
		query_cluster = query_clusters[query.lower()]
	
		for keyword in query_cluster :
			
			if keyword in sentences_per_feature_per_destination[destination_id] :
				
				reviews_list = sentences_per_feature_per_destination[destination_id][keyword]
				
				for review_index in reviews_list :
					if review_index in reviews_per_query_per_destination[destination_id][query] :
						reviews_per_query_per_destination[destination_id][query][review_index] += 1
					else :
						reviews_per_query_per_destination[destination_id][query][review_index] = 1
	
	output = []
	for query in queries :
		
		best_reviews = sorted(reviews_per_query_per_destination[destination_id][query], key=(reviews_per_query_per_destination[destination_id][query]).get, reverse=True)
		
		if len(best_reviews) == 0 :
			continue
		
		output.append('***'+query.upper()+'***')
		for review_index in best_reviews[0:5] :
			output.append('----->'+re.sub(r'[/\\:;\[\]\*]*','', reviews_per_destination[destination_id][review_index])
	
