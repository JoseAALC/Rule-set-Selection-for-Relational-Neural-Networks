
from sklearn.model_selection import train_test_split



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





#separate_in_test_train("facts")
separate_in_test_train("neg")
separate_in_test_train("pos")