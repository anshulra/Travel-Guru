import os,sys,pickle

def rateAspects(sourceDir, sourceDir1,destDir):
	sourceFiles = os.listdir(sourceDir1)
	naspects = 6
	for file in sourceFiles:
		heads = pickle.load(open(sourceDir+"/"+file+".hv",'rb'))
		rev_heads = pickle.load(open(sourceDir+"/"+file+".rhv",'rb'))
		rev_modifiers = pickle.load(open(sourceDir+"/"+file+".rmv",'rb'))
		aspects_d = pickle.load(open(sourceDir+"/"+file+".adh",'rb'))		
		modifiers = pickle.load(open(sourceDir+"/"+file+".mv",'rb'))
		count_h = len(heads)
		count_m = len(modifiers)
		mod_asp_d = pickle.load(open(sourceDir+"/"+file+".mda",'rb'))
		freq = pickle.load(open(sourceDir+"/"+file+".frq",'rb'))
		reviews = pickle.load(open(sourceDir1+"/"+file,'rb'))
		nb = [[[0]*count_m for y in range(naspects)] for x in range(11)]
		Ah = [0]*count_h 
		
		#computing max for assigning aspect group to each head term
		for h in range(count_h):
			asp = aspects_d[0][h]
			pos = 0
			for a in range(1,naspects):
				if aspects_d[a][h] > asp:
						asp = aspects_d[a][h]
						pos = a
			Ah[h] = pos

		#naive bayes counts
		for review in reviews:
			r = int(2*review[0])
			for f in review[1]:
				nb[r][Ah[heads[f[1]]]][modifiers[f[0]]] +=1
			
		
		#normalizing counts
		for r in range(11):
			for a in range(naspects):
				total = sum(nb[r][a])
				if not total == 0:
					for m in range(count_m):
						nb[r][a][m] /= total
		#for m in range(count_m):
		#	for a in range(6):
		#		print(a)				
		#		for r in range(11):
		#			print(str(r)+" "+rev_modifiers[m]+" "+str(nb[r][a][m]))
					
					
		asp_count = [0]*naspects
		asp_rating = [0]*naspects
		
		#computing rating for each aspect
		for review in reviews:
			for f in review[1]:
				#print(f)
				mod = modifiers[f[0]]
				a = Ah[heads[f[1]]]
				asp_count[a] += 1
				rating = 0
				#print(str(a)+" "+str(mod))					
				for r in range(1,11):
					if nb[r][a][mod] > nb[rating][a][mod]:
						rating = r
								
				asp_rating[a] += rating
				#return
		#normalizing aspect ratings with phrase count for that aspect
		for a in range(naspects):
			asp_rating[a]/=2*asp_count[a]

		for h in range(count_h):
			print(('%s \t has rating %f')%(rev_heads[h],asp_rating[Ah[h]]))
		pickle.dump(asp_rating,open(destDir+"/"+file+".rate",'wb'))

if __name__ == "__main__":
	rateAspects(str(sys.argv[1]),str(sys.argv[2]),str(sys.argv[3]))		
