from roaringbitmap import RoaringBitmap
import sys




#performance metrics
class Performance:

	@classmethod
	def calculate_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		TP = rulex_positive[rule_id]
		FP = rulex_negative[rule_id]
		if TP +FP ==0:
			return 0



		metric = TP/(TP+FP)


		return metric

	@classmethod
	def calculate_recall(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		TP = rulex_positive[rule_id]
		FN = n_total_pos - rulex_positive[rule_id]

		if TP +FN ==0:
			return 0

		metric = TP/(TP+FN)
		return metric


	@classmethod
	def calculate_f1(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):

		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall =Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		precisionxrecall = precision*recall
		precisionplusrecall = precision+recall
		
		if precisionplusrecall ==0:
			return 0

		metric = 2* precisionxrecall/precisionplusrecall

		return metric
	
	@classmethod
	def calculate(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		positive_ratio = n_total_neg/n_total_pos
		
		metric = rulex_positive[rule_id]*positive_ratio - rulex_negative[rule_id]
		#print(f"pos: {rulex_positive[rule_id]} neg:{rulex_negative[rule_id]}\nmetric: {metric}")
		
		return metric



#good >= 0.8
#medium >=0.5
#bad <0.5
#acception metrics
class Condition:

	@classmethod
	def bad_recall_good_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0.8<=precision and (0<=recall<0.5):
			return True

		return False

	@classmethod
	def medium_recall_good_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0.8<=precision and (0.5<=recall<0.8):
			return True

		return False

	@classmethod
	def good_recall_good_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0.8<=precision and (0.8<=recall<=1):
			return True

		return False

	#Medium precision

	@classmethod
	def bad_recall_medium_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0.5<=precision<0.8 and (recall<0.5):
			return True

		return False

	@classmethod
	def medium_recall_medium_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0.5<=precision<0.8 and (0.5<=recall<0.8):
			return True

		return False

	@classmethod
	def good_recall_medium_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0.5<=precision<0.8 and (0.8<=recall<=1):
			return True

		return False

	#Bad Precision

	@classmethod
	def bad_recall_bad_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0<=precision<0.5 and (recall<0.5):
			return True

		return False

	@classmethod
	def medium_recall_bad_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0<=precision<0.5 and (0.5<=recall<0.8):
			return True

		return False

	@classmethod
	def good_recall_bad_precision(cls,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		precision = Performance.calculate_precision(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		recall = Performance.calculate_recall(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)

		if 0<=precision<0.5 and (0.8<=recall<=1):
			return True

		return False




# (rule_id,score,total examples covered)

class Bucket:
	def __init__(self,f,accept,L):
		self.f =f
		self.accept = accept
		self.rules = []
		self.maximun_rules_stored=L

		self.minimun_stored = -1000 #high value out of the possible values to the metrics


	def calculate(self,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		if self.accept(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
			return self.f(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)
		else:
			print("Unaceptable rule")
			return 0
		

	def validate_rule(self,rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
		metric = -1
		

		if self.accept(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg):
			metric = self.calculate(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg)


		if metric ==-1:
			return

		old_minimun =self.minimun_stored
		if metric > self.minimun_stored:
			self.minimun_stored = metric

		if len(self.rules)< self.maximun_rules_stored:
			self.rules.append(rule_id)
		else:
			for i in range(len(self.rules)):
				s_metric = self.calculate(self.rules[i],rulex_positive,rulex_negative,n_total_pos,n_total_neg)
				if s_metric == old_minimun:
					self.rules[i] = rule_id
					print("REPLACED")
					break

	def get_rules(self):
		return RoaringBitmap(self.rules)

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



BUCKET_SIZE = 4

buckets = [
	Bucket(Performance.calculate_f1,Condition.bad_recall_good_precision,BUCKET_SIZE),
	Bucket(Performance.calculate_f1,Condition.medium_recall_good_precision,BUCKET_SIZE),
	Bucket(Performance.calculate_f1,Condition.good_recall_good_precision,BUCKET_SIZE),

	Bucket(Performance.calculate_f1,Condition.bad_recall_medium_precision,BUCKET_SIZE),
	Bucket(Performance.calculate_f1,Condition.medium_recall_medium_precision,BUCKET_SIZE),
	Bucket(Performance.calculate_f1,Condition.good_recall_medium_precision,BUCKET_SIZE),

	Bucket(Performance.calculate_f1,Condition.good_recall_bad_precision,BUCKET_SIZE),
	Bucket(Performance.calculate_f1,Condition.medium_recall_bad_precision,BUCKET_SIZE),
	Bucket(Performance.calculate_f1,Condition.bad_recall_bad_precision,BUCKET_SIZE)



]

buckets_c = [0,0,0,0,0,0,0,0,0]

#bucket1 = Bucket(Performance.calculate_precision,Condition.bad_recall_good_precision)




for rule_id in range(len(rules)):
	for i in range(len(buckets_c)):
		buckets[i].validate_rule(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg) 
		#if buckets[i].accept(rule_id,rulex_positive,rulex_negative,n_total_pos,n_total_neg) :
		#	buckets_c[i]+=1


def Union_of_sets(sets):
	initial_set = RoaringBitmap([])

	for i in range(len(sets)):
		initial_set = initial_set.union(sets[i])
	return initial_set

rule_sets = []
for i in range(len(buckets_c)):
	rule_sets.append(buckets[i].get_rules())

final_rules = Union_of_sets(rule_sets)


#chosen_rules = [ rules[i] for i in final_rules]
#print(chosen_rules)


#convert to kaur format
processed_rules =[]
for choosen in final_rules:
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



resulted_file = open("Buckets_out","w")
for rule in processed_rules:
	resulted_file.write(rule + "\n")
resulted_file.close()


