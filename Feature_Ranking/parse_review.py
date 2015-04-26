import os,sys,nltk,re,pickle

def parseData(sourceDir, destDir):
	sourceFiles = os.listdir(sourceDir)
	html_tags = re.compile(r'<[^>]+>')
	count = 0
	grammar = r"""
NP:	{<JJ|JJR|JJS|VBG><NN|NNS>}
	{<RB><JJ>}
	{<RBR|RBS|RB><RB>}
	{<RB|RBR|RBS><VB|VBD|VBG|VBP|VBZ>}
	{<VBP><VBG>}
				
"""	
	chunker = nltk.RegexpParser(grammar)		
	for file in sourceFiles:
		filepath = sourceDir+"/"+file;
		data = pickle.load(open(filepath,'rb'))
		result = []
		for review in data:
			temp = []
			for sent in review[1]:
				psent = chunker.parse(sent)
				print(psent)
			result.append([review[0],temp])	 
		outFile = open(destDir+"/"+file,'w')
		outFile.write(str(result))
		#pickle.dump(data,outFile)
		#outFile.close()
		count += 1
		sys.stderr.write(str(count*100/len(sourceFiles)) +"% completed.\n")

if __name__ == "__main__":
	parseData(str(sys.argv[1]),str(sys.argv[2]))
