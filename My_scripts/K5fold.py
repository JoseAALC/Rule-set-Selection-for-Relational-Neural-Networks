
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold


name = "facts"



def separate_in_test_train(name):

	facts_file = open("test_%s.txt"%name,"r")


	facts = []
	for l in facts_file:
		facts.append(l.replace("\n",""))


	x_80_percent, x_20_percent =  train_test_split(facts, test_size =.50, shuffle  = True)



	file_80 = open("test_%s80.txt"%name,"w")


	for l in x_80_percent:
		file_80.write("%s\n"%l)


	file_80.close()


	file_20 = open("test_%s20.txt"%name,"w")


	for l in x_20_percent:
		file_20.write("%s\n"%l)


	file_20.close()

	facts_file.close()


def fold5(name):
	file = open("full_%s.txt"%name,"r")
	elements = []
	
	for l in file:
		elements.append(l.replace("\n",""))

	#print(elements)

	kf = KFold(n_splits=5)

	splits =kf.split(elements)

	print(splits)


	for i, (train_index,test_index) in enumerate(splits):
		fold_file = open(f"{name}_fold{i+1}.txt","w")
		print(f"Fold {i}:")
		#print(f"  Train: index={train_index}")
		#print(f"  Test:  index={test_index}")
		print(len(test_index))
		foldn =[elements[i] for i in test_index]
		for fe in foldn:
			fold_file.write(f"{fe}\n")
		fold_file.close()
		


	file.close()





fold5("neg")
fold5("pos")
#separate_in_test_train("facts")
#separate_in_test_train("neg")
#separate_in_test_train("pos")