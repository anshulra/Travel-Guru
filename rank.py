
import sys,json,glob,re,math
import gensim,numpy

sentences_per_feature_per_destination = json.load(open("sentences_per_feature_per_destination.json", "r"))
destinations_per_id = json.load(open("all_destinations.json"))
reviews_per_destination = json.load(open("reviews_per_destination.json"))

reviews_per_query_per_destination = {}

def featureRatings(all_ratings,location):
	ratings = []	
	for cluster in all_ratings[location]:
		ratings.append(cluster[0][0]+('\t %.2f')%(cluster[1]))		
	#print(ratings)		
	return ratings

def review_ranking( queries , query_clusters, destination) :
	
	
	for i in destinations_per_id :
		if destinations_per_id[i] == destination :
			destination_id = str(i)
			break
	#for destination_id in destinations :
	reviews_per_query_per_destination[destination_id] = {}	
	for query in queries :
		
		reviews_per_query_per_destination[destination_id][query] = {} 
		
		query_cluster = query_clusters[query.lower()][destination]
	
		for keyword in query_cluster :
			
			if keyword in sentences_per_feature_per_destination[destination_id]:
				
				reviews_list = sentences_per_feature_per_destination[destination_id][keyword]
				
				for review_index in reviews_list :
					if review_index in reviews_per_query_per_destination[destination_id][query] :
						reviews_per_query_per_destination[destination_id][query][review_index] += 1
					else :
						reviews_per_query_per_destination[destination_id][query][review_index] = 1
	

	#for destination_id in destinations :
	output = []
	output.append('---------------------------------------------------------------------------')
	for query in queries :
		output.append('Query: '+query.upper())
		
		best_reviews = sorted(reviews_per_query_per_destination[destination_id][query], key=(reviews_per_query_per_destination[destination_id][query]).get, reverse=True)
		
		for review_index in best_reviews[0:5] :
			output.append('----->'+reviews_per_destination[destination_id][review_index])
		output.append('---------------------------------------------------------------------------')
	
	return output


def rankData(keywordModel,w2vModel,query):
	inFile = open(keywordModel,'r')
	keywords_json = json.load(inFile)
	locations = []
	locScore = []
	clusterDict = {}


	for i in keywords_json:
		locations.append(i)
		locScore.append(0)


	for word in query:
		clusterDict[word] = {}
		for place in locations:
			clusterDict[word][place] = []

	for place in locations:
		keywordList = keywords_json[place]["keywords"]
		tf = 0
		for element in keywordList:
			for component in element:
				tf = tf + component[1]
		keywords_json[place]["doc_length"] = tf


	'''for word in query:
		try:
			wordVec = w2vModel[word]
		except KeyError:
			query.remove(word)
			continue

		for place in locations:
			centroids = keywords_json[place]["centroids"]
			index = locations.index(place)
			looper = 0

			maxVal = 0

			for vector in centroids:
				clusterMembers = keywords_json[place]["keywords"][looper]
				multFactor = 0
				for member in clusterMembers:
					multFactor = multFactor + int(member[1])

				tempVal = (numpy.dot(vector,wordVec))*multFactor

				if tempVal > maxVal:
					maxVal = tempVal
					clusterDict[word][place] = []
					for member in clusterMembers:
						clusterDict[word][place].append(member[0])


				locScore[index] = locScore[index] + tempVal
				looper = looper + 1
			#locScore[index] = locScore[index]/keywords_json[place]["doc_length"]'''

	for word in query:
		try:
			wordVec = w2vModel[word]
		except KeyError:
			query.remove(word)
			continue

		for place in locations:
			centroids = keywords_json[place]["centroids"]
			index = locations.index(place)
			looper = 0

			scoreList = []
			tempVal = 0
			for vector in centroids:
				clusterMembers = keywords_json[place]["keywords"][looper]

				for member in clusterMembers:
					#dotProd = numpy.dot(wordVec,w2vModel[member[0]])
					dotProd = w2vModel.similarity(word,member[0])
					tempVal = tempVal + (dotProd*member[1]/keywords_json[place]["doc_length"])
					#tempVal = tempVal + (dotProd*member[1])
					scoreList.append((dotProd,member[0]))

				looper = looper + 1

			scoreList.sort(reverse=True)

			scoreListWords = []
			for x in scoreList:
				scoreListWords.append(x[1]) 
			clusterDict[word][place] = []
			for k in range(3):
				clusterDict[word][place] = scoreListWords[:3]


			locScore[index] = locScore[index] + tempVal/math.log(keywords_json[place]["doc_length"])
			

	scoreDic = []
	for i in range(len(locations)):
		scoreDic.append((locScore[i],locations[i]))

	scoreDic.sort(reverse=True)

	for i in range(5):
		print '***************************************************************************'
		
		place = scoreDic[i][1]
		'''for word in query:
			print clusterDict[word][place]'''
		summList = review_ranking(query,clusterDict,place)
		with open('featurerating.txt') as feature_infile:
			all_ratings = json.load(feature_infile)
		placeWords = place.split('_')
		placeStr = ""
		for j in placeWords:
			placeStr = placeStr + j + " "
		loc_feature_rating = featureRatings(all_ratings,place)
		print str(i+1) + '. ' + placeStr
		#print '---------------------------------------------------------------------------'
		'''for q in query:
			print q
			print clusterDict[q][place]'''		
		for summ in summList:
			print summ
		print '---------------------------------------------------------------------------'
		print '---------------------------------------------------------------------------'
		for word in loc_feature_rating:
			print "(" ,word ,") ",
		print 
		print '***************************************************************************'

	'''for i in range(len(locations)):
		print str(i)	 + " "+scoreDic[i][1]'''

			
if __name__ == '__main__':
	keywordModel = sys.argv[1]
	W2VFile  = sys.argv[2]
	query = []
	W2Vmodel = gensim.models.Word2Vec.load_word2vec_format(W2VFile, binary=True)
	print "Loaded vectors"

	while 1:
		query = raw_input("Enter Keywords: ").split()
		if len(query) == 0 :
			continue
		else:
			if query[0] == "EXIT":
				break

		rankData(keywordModel,W2Vmodel,query)
