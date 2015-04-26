import os,sys,nltk,re

def crawlData(sourceDir, destDir):
	sourceFiles = os.listdir(sourceDir)
	html_tags = re.compile(r'<[^>]+>')
	for file in sourceFiles:
		filepath = sourceDir+"/"+file;
		inFile = open(filepath,'r')
		data = ""
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
					
					skipLine = False
		outFile = open(destDir+"/"+file,'w')
		outFile.write(result)
		outFile.close()
		inFile.close()

if __name__ == "__main__":
	crawlData(str(sys.argv[1]),str(sys.argv[2]))
