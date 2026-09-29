import numpy as np
import matplotlib.pyplot as plt
 


#checks if a list any duplicate
#returns the list without the dups and the list of duplicate elements
def check_dups(list_data):
	no_dup_list = []
	dups = []
	for i in range(len(list_data)):
		if i+1 < len(list_data):
			if list_data[i] not in list_data[i+1:]:
				no_dup_list.append(list_data[i])
			else:
				
				dups.append(list_data[i])

		else:
			no_dup_list.append(list_data[i])



	return (no_dup_list,dups)


#takes a string with a literal and converts in a dictionary with the name and elements of the literal
def process_literal(literal):
	
	tmp = literal.replace("(", " ").replace(")","").replace(","," ")
	tmp = tmp.split(" ")

	return {"name":tmp[0],"content":tmp[1:]}



#processes a intire list of literals using process_literal function
def process_literal_list(literal_list):
	#print(literal_list)
	return list(map(process_literal,literal_list))



#function called to process the positives negatives and facts files 
def process_literals(file_path):
	literals_file = open(file_path,"r")
	literals =[]
	for literal in literals_file:
		
		tmp = literal.replace(".","").replace(" ","").strip()
		literal_data = process_literal(tmp)

		literals.append(literal_data)

	literals_file.close()
	return literals





#check if any positive is also in the negative set
def cross_check_pos_neg(pos,neg):
	count = 0

	for positive in pos:
		if positive in neg:
			count+=1

	return count






#loads the grounded random walks in a list of {head of the rule, tail of the rule}
def process_grounds(grounded_path):
	grounded_rw= []
	grounded_file= open(grounded_path,"r")

	for rw in grounded_file:
		temp = rw.strip()
		temp = temp[1:len(temp)-1]

		temp = temp.split(":-")

		head = temp[0].strip().replace(" ","")
		body = temp[1].strip().replace(" ","").split("),")
		for i in range(len(body)):
			if body[i][-1]!=")": 
				body[i]+=")"

		grounded = {"head":head,"tail":body}
		grounded_rw.append(grounded)
	return grounded_rw



def extract_var_of_lit(literal):
	new_literal = ""
	inside = False
	for i in range(len(literal)): 
		
		if inside and literal[i]== ")":
			inside =False
			new_literal +="}"
			new_literal+= literal[i]

		
		elif literal[i]== "(":
			inside = True
			new_literal+= literal[i]
			new_literal +="{"

		elif inside and literal[i]== ",":
			new_literal +="}"
			new_literal+= literal[i]
			new_literal+= "{"
		else:
			new_literal+= literal[i]

	return new_literal

		





def extract_variables(list_of_literals):
	variables = set()

	for lit in list_of_literals:
		tmp = lit.split("(")[1].replace(")","").strip().split(",")
		for var in tmp:
			variables.add(var)




	return list(variables)


def process_lifted(lifted_path):
	lifted_file = open("data/lifted.tree","r")
	liteds = []
	for lrw in lifted_file:
		tmp = lrw.strip().replace(" ","").replace(").","")[1:].replace(",!","")
		
		head_tail = tmp.split(":-")
		head = head_tail[0].strip()
		tail= head_tail[1].strip().split("),")
		for i in range(len(tail)):
			if tail[i][-1]!=")": 
				tail[i]+=")"
		lifted = {"head":head,"tail":list(map(extract_var_of_lit,tail)),"variables":extract_variables(tail)}
		
		liteds.append(lifted)



	lifted_file.close()
	return(liteds)



def lifted_rule_satisfability(lifted_rule,positives,negatives,facts):
	def update_variables_state(variables,rule_tail):
		tmp = rule_tail

		for key in variables.keys():
			if variables[key]!=None:
				new_tmp = []
				for literal in tmp:
					print(literal)
					new_tmp.append(literal["content"].replace("{" + str(key) +"}",variables[key]))
				tmp = new_tmp

		return tmp


	rule_tail = process_literal_list(lifted_rule["tail"])
	rule_tail_names = [literal["name"] for literal in rule_tail]
	#print(rule_tail_names)
	#print(process_literal_list(lifted_rule["tail"]))

	filtered_facts = [fact  for fact in facts if fact["name"] in rule_tail_names]
	


	working_positive = positives[0]
	variables_set = {}
	tmp_tail = rule_tail
	for variable in  lifted_rule["variables"]:
		variables_set.update({variable:None})

	print(working_positive)
	variables_set["A"] = working_positive["content"][0]
	variables_set["B"] = working_positive["content"][1]
	print(variables_set)
	print(update_variables_state(variables_set,tmp_tail))


	return None



def same_names(list1,list2):
	if len(list1) == len(list2):
		for i in range(len(list1)):
			if list1[i] != list2[i]:
				return False
		return True
	return False



"""
#FLAGS
NO_DUPS=False
GROUNDED_COVER=True
LIFTED_COVER = True




print("Loading facts...")
facts =process_literals("data/facts.txt")

print("Loading positives...")
positives = process_literals("data/pos.txt")

print("Loading negatives...")
negatives = process_literals("data/neg.txt")

print("Loading grounded random walks...")
grounded_rw =process_grounds("data/Grounded.txt")
print("Loading lifted random walks...")
lifted_rw = process_lifted("data/lifted.tree")


print("\n\nData loaded")
print("facts: " + str(len(facts)))
print("positives: " + str(len(positives)))
print("negatives: " + str(len(negatives)))






grouds_for_each_rw = []

for lift in lifted_rw:
	count=0
	names_lifted =process_literal_list( lift["tail"])
	names_lifted = [ literal["name"] for literal in names_lifted]
	
	for ground in grounded_rw:
		names_grounded = process_literal_list(ground["tail"])
		names_grounded = [ literal["name"] for literal in names_grounded]

		if same_names(names_lifted,names_grounded):
			count+=1
	grouds_for_each_rw.append(count)


mean = sum(grouds_for_each_rw)/len(grouds_for_each_rw)
number_of_unused_lifted = grouds_for_each_rw.count(0)
used = [n for n in grouds_for_each_rw if n !=0]
mean_of_used = sum(used)/len(used)

print("\n\nRandom walk metrics\n---")

print("Number of lifted Random walks: " +str(len(lifted_rw)))
print("Number of grounded Random walks: " +str(len(grounded_rw)))
print("Number of unused lifted Rules: " + str(number_of_unused_lifted))
print("---------------------------------------------------------------")
print("Mean of grouds_for_each_rw: " + str(mean) )
print("Mean of grouds_for_each_rw of used lifted Rules: " + str(mean_of_used))
	
Rules = ["R" + str(i+1) for i in range(len(lifted_rw))]
values = list(grouds_for_each_rw)

fig = plt.figure(figsize = (10, 5))

plt.bar(Rules, values, color ='maroon',
        width = 0.4)
 
plt.xlabel("Lifted Rules")
plt.ylabel("Grounded#")
plt.title("Number of grounded rules generated from each lifted")
plt.savefig('plot of rules.png')









#THIS CHECK NEEDS TO BE DONE BEFORE DOING ANYTHING WITH THE DATA

#Do before

if NO_DUPS:
	print("\n\nRemoving duplicates...")
	facts= check_dups(facts)[0]
	positives= check_dups(positives)[0]
	negatives= check_dups(negatives)[0]



print("\n\nchecking if any positive is in negative set...")
pos_neg=cross_check_pos_neg(positives,negatives)
print("Currently exists: " +str(pos_neg) + " positives in the negative set")




#t = lifted_rule_satisfability( lifted_rw[0], positives, negatives, facts)
#quit()
















print("\n\nchecking cover of random walks...")

negative_c=  0
positives_c= 0
bouth_c = 0


for rw in grounded_rw:

	lit = process_literal(rw["head"])

	positive_cover = lit in positives
	negative_cover = lit in negatives
	#positive_cover = is_literal_on(lit,positives) 
	#negative_cover = is_literal_on(lit,negatives) 

	if positive_cover and negative_cover:
		negative_c+=  1
		positives_c+= 1
		bouth_c += 1
	elif positive_cover:
		positives_c+= 1
	elif negative_cover:
		negative_c+= 1


print("SUMMARY:")
print("Total random walks: " + str(len(grounded_rw)))
print("GRW# in positives: " + str(positives_c))
print("GRW# in negatives: " + str(negative_c))
print("--------------------------------------")
print("Both coverage: " + str(bouth_c/len(grounded_rw) *100))
print("Positive coverage: " + str(positives_c/len(grounded_rw) *100) +"%")
print("Negative coverage: " + str(negative_c/len(grounded_rw) *100)+"%")


positive_cover = [ 0 for i in range(len(positives))]
negative_cover = [ 0 for i in range(len(negatives))]

pos_conter =0
neg_conter =0


import numpy as np
#Rule_positive = np.zeros((len(grounded_rw),len(positives)))
#Rule_negative = np.zeros((len(grounded_rw),len(negatives)))



for i  in range(len(positives)):
	for j in range(len(grounded_rw)):

		lit = process_literal(grounded_rw[j]["head"])
		if lit == positives[i]:
			positive_cover[i]=1
			#Rule_positive[j,i] =1

for i  in range(len(negatives)):
	for j in range(len(grounded_rw)):

		lit = process_literal(grounded_rw[j]["head"])
		if lit == negatives[i]:
			negative_cover[i]=1
			#Rule_negative[j,i] =1


print("\n\nPositives covered by GRW: " + str(sum(positive_cover)))
print("Negatives covered by GRW: " + str(sum(negative_cover)))

print("-------------------------------------------------------")
print("Positives rate covered by GRW: " + str(sum(positive_cover)/len(positive_cover)*100))
print("Negatives covered by GRW: " + str(sum(negative_cover)/len(negative_cover)*100))


#import seaborn as sns

#ax = sns.heatmap(Rule_positive, linewidth=0.5)
#plt.show()


#ax = sns.heatmap(Rule_negative, linewidth=0.5)
#plt.show()

quit()
same_posives = []
same_negatives = []

for i in range(len(grounded_rw)):
	for j in range(i,len(grounded_rw)):
		is_same= True
		for k in range(len(positives)):
			if Rule_positive[i,k] != Rule_positive[j,k] :
				is_same = False

		if is_same:
			same_posives.append((i,j))



for i in range(len(grounded_rw)):
	for j in range(i,len(grounded_rw)):
		is_same= True
		for k in range(len(negatives)):
			if Rule_negative[i,k] != Rule_negative[j,k] :
				is_same = False

		if is_same:
			same_negatives.append((i,j))




same = [e for e in same_posives if e in same_negatives]
print(same)










"""















