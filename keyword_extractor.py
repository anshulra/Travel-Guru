from __future__ import print_function
from alchemyapi import AlchemyAPI
import sys,json,glob,nltk,re



# dumps keywords of all locations into the output file. (JSON) 
# structure of JSON : 
# 		    "location" => { => doc_length =>
#				    => keywords => { word => TF}
#
#


# arguments : 1. directory name to read text	2. output_file
 

# Tokenization
# removal of numericals
#  


def extract_keywords():
	out_file = open(sys.argv[2],"w")
	dir_name = sys.argv[1]
	loc_hash = {}
	alchemyapi = AlchemyAPI()
	for file_in in glob.glob(dir_name+"/*.txt"):
		word_count = {}
		f_obj = open(file_in)
		loc = file_in.split("/")[1].split(".")[0]
		loc_hash[loc] = {}
		
		text = f_obj.read()
		text = text.replace("*******************","")
		doc_len = len(text)
		text_words = text.split()
		unigrams_freq = nltk.FreqDist(text_words)

		bigrams = bgs = nltk.bigrams(text_words)
		bigrams_freq = nltk.FreqDist(bigrams)

		loc_hash[loc]["len"] = doc_len

		print(" calling api for "+file_in + ".......")
		response = alchemyapi.keywords('text', text, {'sentiment': 0})
		if response['status'] == 'OK':
			loc_hash[loc]["keywords"] = {}
			for keyword in response['keywords']:
				words = keyword['text'].split()
				if (len(words) <= 2):
					loc_hash[loc]["keywords"][keyword['text']] = 0
				if len(words) > 1:
					for i in range(len(words)):
						new_word = words[i]
						if new_word not in loc_hash[loc]["keywords"]:
							loc_hash[loc]["keywords"][new_word] = 0
						if (i != len(words)-1): 
							new_word = words[i]+" "+words[i+1]
							if new_word not in loc_hash[loc]["keywords"]:
								loc_hash[loc]["keywords"][new_word] = 0
					
					
		else:
    			print('Error in keyword extaction call for file :' + file_in + " : " + response['statusInfo'])
		myRE = re.compile('^[a-zA-Z]+$')		
		for keyword in loc_hash[loc]["keywords"]:
			words = keyword.split()
			if (len(words) > 1):
				if (re.match(myRE,words[0])):
					if (re.match(myRE,words[1])):
						t = (words[0],words[1])
						freq = bigrams_freq[t]
			else:
				if (re.match(myRE,words[0])):
					freq = unigrams_freq[words[0]]
			
			loc_hash[loc]["keywords"][keyword] = freq	
		
	json.dump(loc_hash,out_file)


if __name__ == '__main__':
	extract_keywords()
