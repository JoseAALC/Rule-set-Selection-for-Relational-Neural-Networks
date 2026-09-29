from roaringbitmap import RoaringBitmap
import sys


#choice =0 calculate
#choice =1 calculate_f1
if len(sys.argv)>1:
	choice = int(sys.argv[1])
else:
	choice =0

#0m0.357s
rules =[]

examples = []

rulex_coversy = []
rulex_positive = []
rulex_negative = []

n_total_pos=0
n_total_neg=0


##READING INPUTS
read_positives = open("full_pos.txt")

for l in read_positives:
	examples.append(l.replace("\n",""))
	n_total_pos+=1



read_positives.close()
read_negatives = open("full_neg.txt")

for l in read_negatives:
	examples.append(l.replace("\n",""))
	n_total_neg+=1

read_negatives.close()


#print(examples)


rule_position= -1





coverage_file = open("UNIQ_List_Coverage.txt")
for l in coverage_file:
	if "Rule" in l:
		if rule_position==-1:
			rule_position =0
		else:
			rule_position+=1

		rulex_coversy.append(RoaringBitmap([]))
		rulex_positive.append(0)
		rulex_negative.append(0)
		
		rules.append(l[6:])


	elif "ExampleP" in l:
		example = l.replace("\n",".")[10:]
		for i in range(len(examples)):
			if example == examples[i]:
				rulex_positive[rule_position]+=1
				rulex_coversy[rule_position].add(i)
				break

	elif "ExampleN" in l:
		example = l.replace("\n",".")[10:]
		for i in range(len(examples)):
			if example == examples[i]:
				rulex_negative[rule_position]+=1
				rulex_coversy[rule_position].add(i)
				break

coverage_file.close()

#print(rulex_coversy)


def calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
	TP = rulex_positive[rule_id]
	FP = rulex_negative[rule_id]
	if TP +FP ==0:
		return 0



	metric = TP/(TP+FP)


	return metric

def calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
	TP = rulex_positive[rule_id]
	FN = n_total_pos - rulex_positive[rule_id]

	if TP +FN ==0:
		return 0

	metric = TP/(TP+FN)
	return metric



def calculate_f1(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):

	precision = calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
	recall =calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

	precisionxrecall = precision*recall
	precisionplusrecall = precision+recall
	
	if precisionplusrecall ==0:
		return 0

	metric = 2* precisionxrecall/precisionplusrecall

	return metric
	

def calculate(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
	positive_ratio = n_total_neg/n_total_pos
	
	metric = rulex_positive[rule_id]*positive_ratio - rulex_negative[rule_id]
	#print(f"pos: {rulex_positive[rule_id]} neg:{rulex_negative[rule_id]}\nmetric: {metric}")
	
	return metric


# (rule_id,score,total examples covered)
def calculate_list(rules_ids,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
	values = [(rule_id,abs(calculate(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)), rulex_positive[rule_id]+ rulex_negative[rule_id]) for rule_id in rules_ids]
	return values


def calculate_list2(rules_ids,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
	values = [(rule_id,abs(calculate_f1(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)), rulex_positive[rule_id]+ rulex_negative[rule_id]) for rule_id in rules_ids]
	return values

def calculate_intersections(rule,candidates,rulex_coversy):
	new_candidates = []
	new_rulex_coversy = {}
	for candidate in candidates:
		#print(f"A:{rulex_coversy[rule]}")
		#print(f"B:{rulex_coversy[candidate[0]]}")
		
		difference = rulex_coversy[candidate[0]].difference(rulex_coversy[rule]) 
		
		#print(f"Difference = {difference}")
		#print(candidate[0])
		#print("-"*20)

		if len(difference)>0:
			new_candidates.append(candidate)
			new_rulex_coversy[candidate[0]]=difference


	return new_candidates,new_rulex_coversy






#Initialization
rules_choosen = []
#calculates the score for each rule
if choice ==0:
	print("Calculate positives negatives difference...")
	candidates_to_next_rule =calculate_list(range(len(rules)),rulex_positive,rulex_negative,n_total_pos,n_total_neg)
else:
	print("Calculate F1..")
	candidates_to_next_rule =calculate_list2(range(len(rules)),rulex_positive,rulex_negative,n_total_pos,n_total_neg)
candidates_to_next_rule.sort(key=lambda x: (-x[1], -x[2]))
#print(candidates_to_next_rule)



while len(candidates_to_next_rule)>0 :

	rules_choosen.append(candidates_to_next_rule[0][0])

	candidates_to_next_rule,rulex_coversy = calculate_intersections(rules_choosen[-1],candidates_to_next_rule,rulex_coversy)


#convert to kaur format
processed_rules =[]
for choosen in rules_choosen:
	rule = rules[choosen]

	head_body = rule.split(":")

	body =head_body[1].strip()

	head = head_body[0]
	name_content =head.split("(")

	content =  name_content[1].replace(")","").strip() 
	content= "(" + ", ".join(content.split(",") + ["0"]) +")"

	head = name_content[0]+ content

	body_parts = body.replace(","," ").split(")")
	body_parts = list(filter(None, body_parts))
	body_parts = [part.strip() for part in body_parts]
	body_parts = [part.split("(") for part in body_parts]

	body_parts =[ part[0]+ "("+", ".join(part[1].split(" ")) +")" for part in body_parts]

	body = ", ".join(body_parts) + " , !)."
	head ="(" + head
	rule = head + " :-  " +body
	rule = rule.replace("twin","_")

	processed_rules.append(rule)






if choice ==0:
	resulted_file = open("chosen_out_calc","w")
elif choice ==1:
	resulted_file = open("chosen_out_f1","w")
for rule in processed_rules:
	resulted_file.write(rule + "\n")

resulted_file.close()


