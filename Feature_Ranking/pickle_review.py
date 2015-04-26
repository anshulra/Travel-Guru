import os,sys,nltk,re,pickle

def crawlData(sourceDir, destDir):
	sourceFiles = os.listdir(sourceDir)
	html_tags = re.compile(r'<[^>]+>')
	amp = re.compile(r'&.+;')
	count = 0
	for file in sourceFiles:
		filepath = sourceDir+"/"+file;
		inFile = open(filepath,'r')
		data = []
		result = ""
		rating = 0
		skipLine = False
		for line in inFile:
			if not skipLine:
				foundreview = line.find('<i class="star-img',0)
				if foundreview > -1:
					loc = line.find('title="')
					rating = float(line[loc+7:loc+10])
					skipLine = True
			else:
				foundreview = line.find('<p itemprop="description" lang="en">',0)
				if foundreview > -1:
					review = html_tags.sub(' ',line)
					review = amp.sub(' ',review)
					review = nltk.sent_tokenize(review)
					review = [nltk.word_tokenize(sent) for sent in review]
					review = [nltk.pos_tag(sent) for sent in review]
					#review = [' '.join([word[0]+"/"+word[1] for word in sent]) for sent in review]
					data.append([rating,review])
					skipLine = False
		outFile = open(destDir+"/"+file,'wb')
		#outFile.write(str(data))
		pickle.dump(data,outFile)
		outFile.close()
		inFile.close()
		count += 1
		sys.stderr.write(str(count*100/len(sourceFiles)) +"% completed.\n")

if __name__ == "__main__":
	crawlData(str(sys.argv[1]),str(sys.argv[2]))
