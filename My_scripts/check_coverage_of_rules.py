from roaringbitmap import RoaringBitmap
import sys


if len(sys.argv)<2:
	print("No file selected with the rules")
	quit()

def convert_rule_format(r):
	#remove initial ( and final ).
	tmp_rule = r[1:-2]

	#separate in head and literals
	tmp_parts = tmp_rule.split(" :-  ")
	
	#prepare the head
	head_tmp= tmp_parts[0]
	head_tmp = head_tmp.replace(", 0)",")").replace(", ",",")
	

	


	#prepare the literals
	literals_tmp= tmp_parts[1].split("),")
	tail = literals_tmp[-1].split(")")[0]
	literals_tmp = literals_tmp[:-1] + [tail]
	literals_tmp = list(map(lambda x:x.replace(" ","").replace("_","twin")+")", literals_tmp))
	literals_tmp = ", ".join(literals_tmp)
	
	
	#recreate the rule by attaching the head to the literals
	tmp_rule = f"{head_tmp}: {literals_tmp}"
	return tmp_rule
	


rules =[]

examples_pos = []
examples_neg = []
rulex_coversy = []
rulex_positive = []
rulex_negative = []

n_total_pos=0
n_total_neg=0


##READING INPUTS
read_positives = open("full_pos.txt")

for l in read_positives:
	examples_pos.append(l.replace("\n",""))
	n_total_pos+=1



read_positives.close()


read_negatives = open("full_neg.txt")
for l in read_negatives:
	examples_neg.append(l.replace("\n",""))
	n_total_neg+=1

read_negatives.close()




#process the rules to check the coverage
read_rules = open(sys.argv[1])

rules_to_check=[]
for r in read_rules:
	new_r = convert_rule_format(r)
	rules_to_check.append(new_r)

read_rules.close()








for r in rules_to_check:
	rulex_positive.append(RoaringBitmap([]))
	rulex_negative.append(RoaringBitmap([]))



#Calculate the coverage for each rule
rule_position=-1
coverage_file = open("UNIQ_List_Coverage.txt")
for l in coverage_file:
	#print(l)
	if "Rule" in l:
		rule_position =-1 
		#print("HERE")
		rule = l[6:]
		#print(rule)
		for i in range(len(rules_to_check)):
			if rules_to_check[i].strip() == rule.strip():
				rule_position = i
				#print(rule_position)
	
	#if the rule in the file is not in the set we want to check
	elif rule_position ==-1:
		continue
	elif "ExampleP" in l:
		example = l.replace("\n",".")[10:]
		for i in range(len(examples_pos)):
			if example == examples_pos[i]:
				#print(rule_position)
				rulex_positive[rule_position].add(i)
				break

	elif "ExampleN" in l:
		example = l.replace("\n",".")[10:]
		for i in range(len(examples_neg)):
			if example == examples_neg[i]:
				rulex_negative[rule_position].add(i)
				break

coverage_file.close()

union_of_positives = RoaringBitmap([])
union_of_negatives = RoaringBitmap([])


for i in range(len(rules_to_check)):
	union_of_positives = union_of_positives.union(rulex_positive[i])
	union_of_negatives = union_of_negatives.union(rulex_negative[i])



print(f"Positives covered: {union_of_positives}")
print(f"Positives number: {len(union_of_positives)}")
print(f"Negatives covered: {union_of_negatives}")
print(f"Negatives number: {len(union_of_negatives)}")
