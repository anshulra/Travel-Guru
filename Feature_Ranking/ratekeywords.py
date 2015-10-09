import json,sys,os,pickle,nltk

def rateKeywords():
	with open('model.txt') as infile:
		locations = json.load(infile)
	naspects = 6
	results = {}
	flag = 0
	dir1 = 'review_aspect_Rating/'
	dir2 = 'clustering_results/'		
	for location in locations.keys():
		flag += 1
		try:
			#print('Printing heads')
			#for h in heads.keys():
			#	print(h)
			#print(location)	
			aspect_rating = pickle.load(open(dir1+location+'.txt.rate','rb'))
			heads = pickle.load(open(dir2+location+'.txt.hv','rb'))
			aspects_d = pickle.load(open(dir2+location+".txt.adh",'rb'))
			count_h = len(heads)
			Ah = [0]*count_h
			s = 0
			for a in range(6):
				s += aspects_d[a][0]
			for h in range(count_h):
				for a in range(1,naspects):
					if aspects_d[a][h] > aspects_d[Ah[h]][h]:
						Ah[h] = a		
			results[location] = []
			cluster_arr = locations[location]['keywords']
			for cluster  in cluster_arr:
				rating = 0
				#rating2 = 0
				count = 0
				#count2 = 0
				words = []
				for word in cluster:
					word = word[0]
					if word in heads:
						#print(heads[word])
						h = heads[word]
						rsum = 0
						psum = 0
						for a in range(naspects):
							rsum += aspect_rating[a]*aspects_d[a][h]
							psum += aspects_d[a][h]
						#print(str(psum))
						if psum > 0:
							count += 1
							rating += rsum/psum
					words.append(word)
				words = nltk.pos_tag(words)
				nouns = []
				for word in words:
					if word[1] == 'NN' or word[1] == 'NNS':
						nouns.append(word[0])
					#print(word[)	 					
				if count > 0 and len(nouns) > 0:
					rating = rating/count
					results[location].append([nouns,rating])
					#print(str(nouns)+'\t'+str(rating))
			#break	
					
		except:
			print('err')
			continue
	#json_str = json.dumps(results)
	#open('featurerating.txt','w').write(json_str)	
if __name__ == "__main__":
	rateKeywords()		
