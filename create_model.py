import sys,json,glob,nltk,re
import word2vec
import gensim


''' RUN WITH PYTHON2.7 '''


''' model file structure : 
	"location_name"=>{ "keywords" => [[],[],[]]
			   "centroids" => [[],[],[]]
			   "document_length" =>

--> keywords is an array where each array represents the words in each cluster.
--> Each array consists of an array of tuples. (word,tf)
'''

# Arguments: arg1:keywords_file	:	arg2:model_file		arg3:vectors.bin file of word2vec	arg4:clusters file of word2vec		arg5:vector dimension

def create_model():
	in_file = open(sys.argv[1])
	out_file = open(sys.argv[2],"w")
	dim = int(sys.argv[5])
	json_data = json.load(in_file)
	final_hash = {}
	model = word2vec.load(sys.argv[3])
	clusters = word2vec.load_clusters(sys.argv[4])

	for loc in json_data:
		count = 0
		keywords = []
		final_hash[loc] = {}
		final_hash[loc]["doc_length"] = json_data[loc]["len"]	
		final_hash[loc]["keywords"] = []
		final_hash[loc]["centroids"] = []
		word_vectors = {}	#"word" => [vector]
		word_clusters = {}	#"cluster_no" => [words]
		cluster_centroids = {}
		print keywords
		for word in json_data[loc]["keywords"]:
			if len(word.split()) > 1:
				continue
			count += 1
			try:
				vec = model[word][:dim]
				cluster_no = clusters[word]
			except KeyError:
				print("No entry in word2vec for " + word)
				continue
			word_vectors[word] = vec
			
			if cluster_no not in word_clusters:
				word_clusters[cluster_no] = []
				cluster_centroids[cluster_no] = dim*[0.0]
			word_clusters[cluster_no].append(word)
			for i in range(dim):
				cluster_centroids[cluster_no][i] += word_vectors[word][i]
		for cluster_no in word_clusters:
			cluster_len = len(word_clusters[cluster_no])
			for i in range(dim):
				cluster_centroids[cluster_no][i] = cluster_centroids[cluster_no][i] / cluster_len
	
		for cluster_no in word_clusters:
			keys = []
			for word in word_clusters[cluster_no]:
				keys.append((word,json_data[loc]["keywords"][word]))
			final_hash[loc]["keywords"].append(keys)
			final_hash[loc]["centroids"].append(cluster_centroids[cluster_no])		
		#print(" Total keywords in " + loc + " : " + str(count))
		#print(" Total word vectors in " + loc + " : " + str(len(word_vectors)))	
		

	
	json.dump(final_hash,out_file)
			
			
if __name__ == '__main__':
	create_model()
