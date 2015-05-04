import os,sys,nltk,re

def parseData(sourceDir, destDir):
	sourceFiles = os.listdir(sourceDir)
	myRE = re.compile('^[a-zA-Z]+$')

	for file in sourceFiles:
		filepath = sourceDir+file;
		inFile = open(filepath,'r',errors="ignore")

		data = ""
		for line in inFile:
			data = data + ' ' + line

		tokens = nltk.word_tokenize(data)

		outFile = open(destDir+file,'w')

		for token in tokens:
			#if myRE.match(token):
			#	outFile.write(token.lower() + ' ')
			outFile.write(token.lower() + ' ')

		outFile.close()
		inFile.close()

if __name__ == "__main__":
	parseData(str(sys.argv[1]),str(sys.argv[2]))
