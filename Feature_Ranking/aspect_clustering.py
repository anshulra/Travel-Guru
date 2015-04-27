#implementation of PLSA for clustering aspects
import os,sys,pickle,random
def clusterAspects(sourceDir, destDir):
	sourceFiles = os.listdir(sourceDir)
	count = 0
	naspects = 8
	for file in sourceFiles:
		filepath = sourceDir+"/"+file;
		data = pickle.load(open(filepath,'rb'))
		heads = {}
		rev_heads = []	
		modifiers = {}
		rev_modifiers = []
		count_h = 0
		count_m = 0
		for review in data:
			for pair in review[1]:
				if not pair[0].lower() in modifiers:
					modifiers[pair[0]] = count_m
					rev_modifiers.append(pair[0])
					count_m +=1
				if not pair[1].lower() in heads:
					heads[pair[1]] = count_h
					rev_heads.append(pair[1])
					#print(pair[0]+" "+pair[1])
					count_h +=1
			
		freq = [[0]*count_h for x in range(count_m)]
		for review in data:
			for pair in review[1]:
				indx = modifiers[pair[0].lower()]
				indy = heads[pair[1].lower()]
				freq[indx][indy]+=1
		joint_d = [[[0]*naspects for x in range(count_h)] for y in range(count_m)]
		mod_asp_d = [[0]*naspects for x in range(count_m)]
		aspects_d = [[0]*count_h for x in range(naspects)]
		
		#random start
		random.seed()

		for m in range(count_m):
			total = 0
			for a in range(naspects):
				mod_asp_d[m][a] = random.random()
				total += mod_asp_d[m][a]
			for a in range(naspects):
				mod_asp_d[m][a] = mod_asp_d[m][a]/total

		for m in range(count_m):
			for h in range(count_h):
				total = 0
				for a in range(naspects):
					joint_d[m][h][a] = random.random()
					total += joint_d[m][h][a]
				for a in range(naspects):
					joint_d[m][h][a] /= total
		
		for a in range(naspects):
			total = 0
			for h in range(count_h):
				aspects_d[a][h] = random.random()
				total += aspects_d[a][h]
			for h in range(count_h):
				aspects_d[a][h] /= total	
			
		for i in range(100):
			#E step
			#print(('iteration %u')%(i))
			flag = True
			for m in range(count_m):
				for h in range(count_h):
					total = 0
					for a in range(naspects):
						total += mod_asp_d[m][a]*aspects_d[a][h]
					if total == 0:
						break
					for a in range(naspects):
						joint_d[m][h][a] = mod_asp_d[m][a]*aspects_d[a][h]/total
				#M1 step
			for m in range(count_m):
				tempasp = [0]*naspects
				total = 0	
				for a in range(naspects):
					for h in range(count_h):
						tempasp[a] += freq[m][h]*joint_d[m][h][a]
						#print(str(freq[m][h]))
					total += tempasp[a]
				for a in range(naspects):
					mod_asp_d[m][a] = tempasp[a]/total
			#M2 step
			delta = 0
			for a in range(naspects):
				temph = [0]*count_h
				total = 0
				for h in range(count_h):
					for m in range(count_m):
						temph[h] += freq[m][h]*joint_d[m][h][a]  
					total += temph[h]
				for h in range(count_h):
					old = aspects_d[a][h]	
					aspects_d[a][h] = temph[h]/total
					delta += abs(old-aspects_d[a][h])
			if (delta/(naspects*count_h) < 0.000001):
				break
		pickle.dump(heads,open(destDir+"/"+file+".hv",'wb'))
		pickle.dump(rev_heads,open(destDir+"/"+file+".rhv",'wb'))
		pickle.dump(modifiers,open(destDir+"/"+file+".mv",'wb'))
		pickle.dump(rev_modifiers,open(destDir+"/"+file+".rmv",'wb'))
		pickle.dump(aspects_d,open(destDir+"/"+file+".adh",'wb'))
		pickle.dump(joint_d,open(destDir+"/"+file+".joint",'wb'))
		pickle.dump(mod_asp_d,open(destDir+"/"+file+".mda",'wb'))
		count += 1
		sys.stderr.write(str(count*100/len(sourceFiles)) +"% completed.\n")
		
if __name__ == "__main__":
	clusterAspects(str(sys.argv[1]),str(sys.argv[2]))
