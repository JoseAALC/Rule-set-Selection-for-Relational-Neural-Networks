
import random
import re
import os 


random.seed(1)
NUMBER_PER_EXAMPLE =100000

pos_f = open("test_pos.txt","r")
neg_f = open("test_neg.txt","r")

examples = []
pos_examples =[]
neg_examples = []
pattern = r"\((.*?)\)"
for l in pos_f:
	match = re.search(pattern, l)
	result = match.group(1)
	pos_examples.append(result)
for l in neg_f:
	match = re.search(pattern, l)
	result = match.group(1)
	neg_examples.append(result)


neg_f.close()
pos_f.close()

examples = pos_examples + neg_examples	

print(f"{len(examples)} examples processed.")



grounds_per_example = {}
for example in examples:
	grounds_per_example[example] = []

del examples

ground_f = open("OutputRW.txt","r")



lift_grounds = {}

for l in ground_f:
	#print(l)
	body= l.split(":-")[0].strip()[1:]
	#print(body)
	match = re.search(pattern, body)
	result = match.group(1).replace(" ","")

	#generate lift string
	create_lift= l.split(":-")[1].strip()
	parts = create_lift.split(")")
	parts[:] = [x for x in parts if x]
	parts[:] = [x.split("(")[0].replace(",", "").strip() for x in parts]
	#print(l.split(":-")[1].strip())
	lift = ",".join(parts)
	


	if lift in lift_grounds.keys():
		#print(lift_grounds[lift])
		if result in lift_grounds[lift].keys():
			lift_grounds[lift][result].append(l)
		else:
			lift_grounds[lift][result] = [l]

	else:
		lift_grounds[lift] = {}
		lift_grounds[lift][result]=[l] 

	#print(lift_grounds)
	#print()
	#print()


	if result in grounds_per_example:
		grounds_per_example[result].append(l)
	else:
		print(f"The key: {result} was not found on examples")


ground_f.close()




def calculate_lift_coverage(lift_grounds, lift,pos_examples,neg_examples):
	n_pos = 0
	n_neg = 0 

	for example in lift_grounds[lift].keys():
		if example in pos_examples:
			n_pos+=1
		elif example in neg_examples:
			n_neg+=1
		else:
			print(f"Example not found")

	#print(f"positives: {n_pos} negatives: {n_neg}")
	return {"positives": n_pos, "negatives": n_neg}
	
def calculate_weight(lift_grounds,lift,pos_examples,neg_examples):
	pos_neg = calculate_lift_coverage(lift_grounds, lift,pos_examples,neg_examples)


	positive_value = len(pos_examples)/len(neg_examples)

	metric = pos_neg["positives"]*positive_value - pos_neg["negatives"]

	#print(f"value: {positive_value}, metric: {metric}")

	return abs(metric)


all_grounds = []
candidates_to_grounds= []

total = 0
for example in grounds_per_example.keys():
	firs_ground =True
	for lift in lift_grounds.keys():
		metric_value = calculate_weight(lift_grounds,lift,pos_examples,neg_examples)
		if example in lift_grounds[lift].keys():
			#print("EXAMPLE")
			grounds_total =0
			grounds = []
			total+=len(lift_grounds[lift][example])
			for instanced_example in lift_grounds[lift][example]:
				if firs_ground==True:
					print(f"E:{example}")
					all_grounds.append(instanced_example)
					firs_ground=False
				#print(instanced_example)
				else:
					#print("K")
					grounds.append((instanced_example,metric_value))


			#print(f"G:{len(grounds)}")
			candidates_to_grounds = candidates_to_grounds+ grounds

#print("-"*20)
#print(candidates_to_grounds)
#print(total)


#print(len(all_grounds))

#print(len(all_grounds))
#print(candidates_to_grounds)

accumulator =[candidates_to_grounds[0][1]]*len(candidates_to_grounds)
#print(len(accumulator))
#print(len(candidates_to_grounds))

for i in range(len(candidates_to_grounds)-1):
	accumulator[i+1]= accumulator[i]+candidates_to_grounds[i][1]

max_value = accumulator[-1]



print(f"Max value: {max_value}")


#print(accumulator)


if NUMBER_PER_EXAMPLE < len(candidates_to_grounds):
	#Choose NUMBER_PER_EXAMPLE
	for i in range(NUMBER_PER_EXAMPLE):
		choice =random.uniform(0, max_value)
		#print(f"C:{choice}")
		for j in range(len(accumulator)):
			if accumulator[j] > choice:

				if candidates_to_grounds[j][0] not in all_grounds:
					all_grounds.append(candidates_to_grounds[j][0])
				decrement = candidates_to_grounds[j][1]
				#print(f"D:{decrement}")

				#Not choose that again
				accumulator[j]=-1
				for k in range(j+1,len(accumulator)):
					if accumulator[k]==-1:
						continue
					if accumulator[k] - decrement<0:
						#print("HELP")
						print(f"k:{k}, accumulator:{accumulator[k]}")
						quit()
					accumulator[k]-=decrement

				max_value = accumulator[-1]
				break
else:

	#print(f"ALL:{len(all_grounds)} , candidates: {len(candidates_to_grounds)}")
	#print(all_grounds)
	for ground in candidates_to_grounds:
		if ground not in all_grounds:
			all_grounds.append(ground[0])
		
	

#print(accumulator)
#print(len(all_grounds))

new_ground_cont = len(all_grounds)
#sample from the weighted population









print(f"New calculated lines are {new_ground_cont} from the initial lines of {total} making a reduction of {100*(1-(float)(new_ground_cont)/total):.3f}%")





#BACKUP OF OutputRW.txt
if not os.path.isfile("BACK_OutputRW.txt"):
	ground_f = open("OutputRW.txt","r")
	back_ground_f = open("BACK_OutputRW.txt","w")

	for l in ground_f:
		back_ground_f.write(l)

	ground_f.close()
	back_ground_f.close()
else:
	print("BACK_OutputRW.txt already exists. Terminating the program")
	quit()








#print(all_grounds)



#MODIFIING THE OutputRW.txt
ground_f = open("OutputRW.txt","w")

for ground in all_grounds:
	print(f"G:{ground}")
	ground_f.write(ground)


ground_f.close()

print("OutputRW.txt was rewrited")
