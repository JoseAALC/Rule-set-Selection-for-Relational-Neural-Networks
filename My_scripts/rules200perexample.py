
import random
import re

random.seed(1)
NUMBER_PER_EXAMPLE =200

pos_f = open("test_pos.txt","r")
neg_f = open("test_neg.txt","r")

examples = []
pos_examples =[]
neg_examples = []
pattern = r"\((.*?)\)"
for l in pos_f:
	match = re.search(pattern, l)
	result = match.group(1)
	examples.append(result)
for l in neg_f:
	match = re.search(pattern, l)
	result = match.group(1)
	examples.append(result)


neg_f.close()
pos_f.close()



print(f"{len(examples)} examples processed.")



grounds_per_example = {}
for example in examples:
	grounds_per_example[example] = []

del examples

ground_f = open("OutputRW.txt","r")

for l in ground_f:
	#print(l)
	body= l.split(":-")[0].strip()[1:]
	#print(body)
	match = re.search(pattern, body)
	result = match.group(1).replace(" ","")
	if result in grounds_per_example:
		grounds_per_example[result].append(l)
	else:
		print(f"The key: {result} was not found on examples")


ground_f.close()
counter =0
number_of_examples_covered =0
count_lines =0
for key in grounds_per_example.keys():
	
	count_lines +=len(grounds_per_example[key])
	if len(grounds_per_example[key]) >0:  
		number_of_examples_covered+=1
		print(f"Example {key} has {len(grounds_per_example[key])} grounds")
	counter+=1

	if len(grounds_per_example[key]) > NUMBER_PER_EXAMPLE:
		grounds_per_example[key] = random.sample(grounds_per_example[key],NUMBER_PER_EXAMPLE)



print(f"Total {number_of_examples_covered} covered examples from a total of {counter} making a aproximated coverage of {100*(float)(number_of_examples_covered)/counter:.3f}%")


count_lines_new =0
for key in grounds_per_example.keys():
	count_lines_new +=len(grounds_per_example[key])


print(f"New calculated lines are {count_lines_new} from the initial lines of {count_lines} making a reduction of {100*(1-(float)(count_lines_new)/count_lines):.3f}%")


ground_f = open("OutputRW.txt","w")

for key in grounds_per_example.keys():
	for l in grounds_per_example[key]:
		ground_f.write(l)


ground_f.close()

print("OutputRW.txt was rewrited")
