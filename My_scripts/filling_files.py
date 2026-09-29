

father_f = open("true_rules.tree","r")


N=1


for l in father_f:
	f = open("T%d"%N , "w")
	f.write(l)
	f.close()
	N+=1

father_f.close()