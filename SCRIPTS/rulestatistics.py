import matplotlib.pyplot as plt
import os
import scores
import numpy as np
from rules import Rule
from literals import Literal
from coverage import Coverage
from logger import Logger
from aleph_example import Aleph_Example
import time
from scores import Positivec,Negativec,Percentages
from venn import venn
import pandas as pd
from upsetplot import plot

class Rule_Statistics:
	def __init__(self, rules,facts,positives,negatives,lifts):

		self.rules = rules
		self.facts = facts
	
		self.positives = [ Literal(lit) for lit in positives]
		self.negatives = [ Literal(lit) for lit in negatives]


		#print(lifts[0])
		#print("*"*20)
		#print(rules[0])
		#quit()

		self.lifts =lifts
		self.__rule_id =0


		#indexing posives/negatives to rules id the  that it covers
		self.__rule_positives = Aleph_Example(self.positives)
		self.__rule_negatives = Aleph_Example(self.negatives)

		self.__coverage = {}


		#indexing pos->rule_indexes that covers it
		#self.pos_rule = [[] for lit in positives ]
		#self.neg_rule = [[] for lit in negatives]


		self.__dettach_rules_from_other_info()
		


		#self.__calculate_coverage()
		
		self.__set_working_enviorment()



	
	
	#public

	def show_rule_coverage(self,log,rules=None):
		if rules==None:
			rules = self.rules

		log.write("COVERAGE_STUDY: (POSITIVES: %d NEGATIVES: %d" %(len(self.positives), len(self.negatives)   )  )
		log.write("-"*20)
		for rule in rules:
			log.write("Rule #%d - %s COVERS: %s" % (rule.get_id(),rule,self.__coverage[rule.get_id()] ))
		log.write("-"*20)
		log.write("\n")


	def write_coverage(self,log,rules=None):
		if rules==None:
			rules = self.rules
		
		
		for rule in rules:
			log.write(f"Rule: {rule}")
			for i in range(len(self.positives)):
				if rule.get_id() in self.__rule_positives.get_rule_ids(self.positives[i]):
					log.write(f"ExampleP: {self.positives[i]}")
			for i in range(len(self.negatives)):
				if rule.get_id() in self.__rule_negatives.get_rule_ids(self.negatives[i]):
					log.write(f"ExampleN: {self.negatives[i]}")



		#for i in range(len(self.positives)):
		#	print(self.__rule_positives.get_rule_ids(self.positives[i]))
		#	if len(self.__rule_positives.get_rule_ids(self.positives[i])) ==0:
		#		count+=1

		#print(len(self.positives))


	#TODO: include negatives
	def show_weak_rules(self,log,rules=None):
		if rules==None:
			rules = self.rules

		log.write("STUDY OF WEAK RULES:")
		log.write("A weak rule is any rule with 0 positive coverage")
		log.write("-"*20)
		total_weak = 0
		for rule in rules:
			if self.__coverage[rule.get_id()].get_positive() ==0:
				log.write("Rule #%d - %s COVERS: %s" % (rule.get_id(),rule,self.__coverage[rule.get_id()]))
				total_weak+=1

		log.write("We found a total of %d weak rules in %d for positives\n"%(total_weak,len(self.rules)))
		log.write("-"*20)
		total_weak = 0
		log.write("A weak rule is any rule with all negatives coverage")
		for rule in self.rules:
			if self.__coverage[rule.get_id()].get_FP() == len(self.negatives):
				log.write("Rule #%d - %s COVERS: %s" % (rule.get_id(),rule,self.__coverage[rule.get_id()]))
				total_weak+=1
		log.write("We found a total of %d weak rules in %d for negatives\n"%(total_weak,len(self.rules)))
		log.write("-"*20)
		log.write("\n")


	def show_uncoveraded_examples(self,log,used_rules =None):
		if used_rules==None:
			used_rules=self.rules

		#TODO adapt this

		log.write("EXAMPLES_UNCOVERED_STUDY: (POSITIVES: %d NEGATIVES: %d" %(len(self.positives), len(self.negatives)   )  )
		log.write("-"*20)

		log.write("POSITIVES:")
		count =0
		

		for i in range(len(self.positives)):
			if len(self.__rule_positives.get_rule_ids(self.positives[i])) ==0:
				log.write("Positive #%d - %s " % (i,self.positives[i]))
				count+=1
		

		log.write("We have %d positive examples that are not covered by any rule."%count)
		log.write("-"*20)
		log.write("NEGATIVES:")
		
		count =0
		for i in range(len(self.negatives)):
			if len(self.__rule_negatives.get_rule_ids( self.negatives[i])) ==0:
				log.write("Negative #%d - %s " % (i,self.negatives[i]))
				count+=1


		log.write("We have %d negative examples that are not covered by any rule."%count)
		log.write("-"*20)
		log.write("\n")


	def show_number_of_rules_covering_examples(self,log):
		log.write("COVERED_BY_RULES_STUDY:")
		log.write("-"*20)
		
		log.write("POSITIVES:")
		for i in range(len(self.positives)):
			log.write("Positive #%d - %s covered by %d rules" % (i,self.positives[i],len(self.__rule_positives.get_rule_ids( self.positives[i]))))
		log.write("NEGATIVES:")
		for i in range(len(self.negatives)):
			log.write("Negative #%d - %s covered by %d rules" % (i,self.negatives[i],len(self.__rule_negatives.get_rule_ids( self.negatives[i]))))

		log.write("-"*20)
		log.write("\n")


	def Rank_Rules_by_score(self,score_used,log,rules=None,):
		scores = self.__calculate_score(score_used,rules)
		scores = sorted(scores,key=lambda item: item[1])
		log.write("SORTED_BY_SCORE %s:" % (type(score_used).__name__))
		log.write("-"*20)

		for score in scores:
			log.write("Rule #%d - %s Score: %s" % (score[0].get_id(),score[0],score[1]))
		log.write("-"*20)
		log.write("\n")


		
		
		self.get_outliers(score_used,Logger(log.file.replace(".txt","") + "OUTLIERS.txt"),rules)


	def number_of_rules_of_each_size(self,log,used_rules=None):
		log.write("NUMBER OF RULES BY SIZE:")
		log.write("-"*20)

		for i in [2,3,4,5,6]:
			log.write("RULES LENGTH: %d - #%d" %(i,len(self.slice_rules_by_size(i,used_rules))))


		log.write("-"*20)
		log.write("\n")


	def get_outliers(self,score,log,rules=None):
		log.write("OUTLIERS:")
		log.write("-"*20)
		scores = self.__calculate_score(score,rules)
		scores_vals = sorted(self.__extract_values_of_score_list(scores))
		
		outlier_list = []
		print(type(score).__name__)
		Q1=np.quantile(scores_vals,0.25)
		Q3=np.quantile(scores_vals,0.75)


		IQR = Q3-Q1

		upper_bound = Q3+(1.5*IQR)
		lower_bound = Q1-(1.5*IQR)

		print("Q1: %f"%Q1)
		print("Q3: %f"%Q3)
		
		print("Upper:%f" % upper_bound)
		print("Lower:%f"%lower_bound)
		

		sorted_rules= sorted(scores, key=lambda x: -x[1])
		log.write("UPPER BOUND OUTLIERS:")
		log.write("-"*20)
		is_upper = True
		for rule_score in sorted_rules:
			if rule_score[1] >upper_bound:
				log.write("Rule #%d - %s Score: %s" % (rule_score[0].get_id(),rule_score[0],rule_score[1]))
				outlier_list.append(rule_score)

			elif rule_score[1] <lower_bound:
				if is_upper:
					is_upper = False
					log.write("\n")
					log.write("LOWER BOUND OUTLIERS:")
					log.write("-"*20)
				log.write("Rule #%d - %s Score: %s" % (rule_score[0].get_id(),rule_score[0],rule_score[1]))
				outlier_list.append(rule_score)







		return outlier_list

	def get_rule_info(self,log,rules=None):
		if rules ==None:
			rules = self.rules

		for rule in rules:
			log.write("Rule #%d - %s" %(rule.get_id(),rule))
			log.write("Coverage %s" % self.__coverage[rule.get_id()])

	def get_origins(self,log):
		count_origins =0
		for rule in self.rules:
			degree_of_rule = self.calculate_degree(rule)

			if degree_of_rule == 0:
				count_origins+=1
				log.write("Rule #%d - %s\nLength: %d"%(rule.get_id(),rule,rule.length()))

		log.write("\n\n")
		log.write("-"*20)
		log.write("%d origins where found\nWe call origin any rule that is not a subrule of any other rule"%count_origins)
		log.write("We had a total of %d rules and from that %f%s are origins"% ( len(self.rules), 100 * count_origins/len(self.rules),"%" ))

	

	def equivalent_rules(self,log,equivalences=None):
		remaining_rules = []
		count =0
		rules_with_equivalents =0
		for i in range(len(self.rules)):
			equivalents_t = False
			for j in range(i+1,len(self.rules)):
				if self.rules[i].same_rule(self.rules[j],equivalences):
					count+=1
					log.write("%d# %s "%(self.rules[i].get_id(),self.rules[i]))
					log.write("%d# %s "%(self.rules[j].get_id(),self.rules[j]))
					log.write("\n")
					equivalents_t = True
			if equivalents_t:
				rules_with_equivalents +=1
			else:
				remaining_rules.append(self.rules[i])

		print(len(remaining_rules))
		log.write("\n\n")
		log.write("-"*20)
		
		log.write("%d rules out of %d rules have an equivalent rule"%(rules_with_equivalents,len(self.rules)))
		log.write("%d equivalent rules found"%count)




		f = open("data/lifted_uniq.tree","w")
		for rule in remaining_rules:
			f.write(rule.kaur_format()+"\n")

		f.close()











		return (count,remaining_rules)





	#PLOTS
	def plot_score(self,scores_list,prefix = "", rules=None):
		computation_of_scores = {}


		for score in scores_list:
			computation_of_scores[type(score).__name__] = self.__extract_values_of_score_list( self.__calculate_score(score,rules))
	

		#if rules !=None:
		#	if rules[0].length()==2:
		#		print("SSSS")
		#		print(rules)
		#		print(computation_of_scores)



		fig, ax = plt.subplots()
		ax.boxplot(computation_of_scores.values(),showmeans=True)
		ax.set_xticklabels(computation_of_scores.keys())
		ax.set_ylim([0, 1])
		
		if isinstance(scores_list[0],Negativec) or isinstance(scores_list[0],Positivec):
			plt.title('number of positives: %d number of negatives: %d'%(len(self.positives),len(self.negatives)    )        ,fontsize = 8,loc="left")

		if isinstance(scores_list[0],Percentages):
			ax.set_ylim([-1, 1])

		plt.title('number of positives: %d number of negatives: %d'%(len(self.positives),len(self.negatives)    )        ,fontsize = 8,loc="left")
		path = os.path.join("plots",(prefix+ "_".join([type(score).__name__ for score in scores_list] ))   )
		plt.savefig(path)
		plt.close()




	def plot_scores_for_all_sizes(self,scores_list,prefix="",rules =None):
		all_rules = {
			2:self.slice_rules_by_size(2,rules),
			3:self.slice_rules_by_size(3,rules),
			4:self.slice_rules_by_size(4,rules),
			5:self.slice_rules_by_size(5,rules),
			6:self.slice_rules_by_size(6,rules)
		}

		self.plot_score(scores_list,prefix=prefix+"length 2: ",rules = all_rules[2])
		self.plot_score(scores_list,prefix=prefix+"length 3: ",rules = all_rules[3])
		self.plot_score(scores_list,prefix=prefix+"length 4: ",rules = all_rules[4])
		self.plot_score(scores_list,prefix=prefix+"length 5: ",rules = all_rules[5])
		self.plot_score(scores_list,prefix=prefix+"length 6: ",rules = all_rules[6])




	def calculate_average_degree(self,log,rules=None):
		if rules ==None:
			rules = self.rules

		if len(rules)==0:
			log.write("Average Degree of Rules: 0")
			return;

		list_of_degrees = []
		for r1 in rules:
			degree = self.calculate_degree(r1)
			

			log.write("rule %s degree: %d." %(r1,degree))
			
			log.write("-"*20)
			log.write("\n")
			list_of_degrees.append(degree)

		log.write("Average Degree of Rules: %d" %(sum(list_of_degrees)/len(list_of_degrees)  ))

	
	def calculate_all_sizes_average_degree(self):

		all_rules = {
			2:self.slice_rules_by_size(2),
			3:self.slice_rules_by_size(3),
			4:self.slice_rules_by_size(4),
			5:self.slice_rules_by_size(5)
		}

		print("SIZE: 2")
		self.calculate_average_degree(Logger("degree_2.txt"),all_rules[2])
		print("SIZE: 3")
		self.calculate_average_degree(Logger("degree_3.txt"),all_rules[3])
		print("SIZE: 4")
		self.calculate_average_degree(Logger("degree_4.txt"),all_rules[4])
		print("SIZE: 5")
		self.calculate_average_degree(Logger("degree_5.txt"),all_rules[5])


	def calculate_degree(self,rule):
		counter = 0
		for other in self.rules:

			if rule.is_subrule(other):
				counter +=1
		return counter

	def calculate_improvements_for_all_sizes(self,score):
		all_rules = {
			2:self.slice_rules_by_size(2),
			3:self.slice_rules_by_size(3),
			4:self.slice_rules_by_size(4),
			5:self.slice_rules_by_size(5)
		}

		#print("SIZE: 2")
		self.calculate_average_improvement_of_childs(score,all_rules[2],Logger("improvement_size_2.txt"))
		#print("SIZE: 3")
		self.calculate_average_improvement_of_childs(score,all_rules[3],Logger("improvement_size_3.txt"))
		#print("SIZE: 4")
		self.calculate_average_improvement_of_childs(score,all_rules[4],Logger("improvement_size_4.txt"))
		#print("SIZE: 5")
		self.calculate_average_improvement_of_childs(score,all_rules[5],Logger("improvement_size_5.txt"))

	def slice_rules_by_size(self,size,rules_used =None):
		new_rules = []
		if rules_used ==None:
			rules_used=self.rules

		for rule in rules_used:
			if rule.length() == size:
				new_rules.append(rule)

		return new_rules

	def calculate_average_improvement_of_childs(self,score,rules=None,log_file=None):
		if rules ==None:
			rules = self.rules

		if len(rules)==0:
			log_file.write("Average improvement of Rules: 0")
			return;

		list_of_improvements = []
		improvements =0
		for r1 in rules:
			score_value = score.calculate(r1,self.__coverage[r1.get_id()])
			for r2 in self.rules:
					if r1.is_subrule(r2):
						
						print("R1 :%s"% r1)
						print("R2 :%s"% r2)
						
						child_score_value = score.calculate(r2,self.__coverage[r2.get_id()])
						improvement = child_score_value-score_value
						if improvement>0:
							improvements+=1
						log_file.write("Father rule %s scored: %f.\n" %(r1,score_value))
						log_file.write("Child  rule %s scored: %f.\n" %(r2,child_score_value))
						log_file.write("Improvement registed : %f.\n" %(improvement))
						log_file.write("-"*20)
						log_file.write("\n\n")

						list_of_improvements.append(improvement)

		log_file.write("Number of improvement found: %d" %(improvements))
		print("SASASSA")
		if len(list_of_improvements) ==0:
			log_file.write("Average improvement of Rules: 0")
			return;

		log_file.write("Average improvement of Rules: %f" %(sum(list_of_improvements)/len(list_of_improvements)  ))


	def calculate_correlations_all_rules(self,used_rules =None,log_file=None,limits=None):
		if used_rules==None:
			used_rules=self.rules

		if log_file==None:
			log_file=Logger()
		
		if limits==None:
			range_to_search = [0,len(used_rules)]
		else:
			range_to_search = limits 

		Number_of_rules_correlated = 0
		for i in range(range_to_search[0],range_to_search[1]):
			for j in range(i+1,len(used_rules)):
				calculate_corr = self.calculate_correlations(used_rules[i],used_rules[j])
				if calculate_corr ==1:
					Number_of_rules_correlated += 1
					log_file.write("Rule id %d rule id %d are %d" % (used_rules[i].get_id(),used_rules[j].get_id(), calculate_corr    )   )
		log_file.write("We find a total of %d rules correlated."%Number_of_rules_correlated)

	def calculate_correlations(self,rule1,rule2):
		
		for i in range(len(self.positives)):
			is_in_rule1 = rule1.get_id() in self.__rule_positives.get_rule_ids(self.positives[i])
			is_in_rule2 = rule2.get_id() in self.__rule_positives.get_rule_ids(self.positives[i])

			if is_in_rule1!=is_in_rule2:
				return 0


		for i in range(len(self.negatives)):
			is_in_rule1 = rule1.get_id() in self.__rule_negatives.get_rule_ids(self.negatives[i])
			is_in_rule2 = rule2.get_id() in self.__rule_negatives.get_rule_ids(self.negatives[i])

			if is_in_rule1!=is_in_rule2:
				return 0
		return 1
			
	def calculate_pos_neg_covered(self,rule_id):
		pos_rules = []
		neg_rules = []
		pos_rules2= []
		pair = [-1,-1]
		neg_rules2 = []
		

		for i in range(len(self.positives)):
			if rule_id in self.__rule_positives.get_rule_ids(self.positives[i]):
				if pair[0] == -1 and pair[1] == -1:
					pair[0] = i
					pair[1] = i
				elif pair[1]+1 == i:
					pair[1] =i
				else:
					if pair[0] == pair[1]:
						pos_rules2.append([pair[0]])
					else:
						pos_rules2.append(pair)
					pair = [i,i]

				pos_rules.append(i)
		if pair[0] == pair[1]:
			pos_rules2.append([pair[0]])
		else:
			pos_rules2.append(pair)
		#print("P-"*20)
		#print(pos_rules2)
		#print(pos_rules)


		pair = [-1,-1]
		for i in range(len(self.negatives)):
			if rule_id in self.__rule_negatives.get_rule_ids(self.negatives[i]):
				if pair[0] == -1 and pair[1] == -1:
					pair[0] = i
					pair[1] = i
				elif pair[1]+1 == i:
					pair[1] =i
				else:
					if pair[0] == pair[1]:
						neg_rules2.append([pair[0]])
					else:
						neg_rules2.append(pair)
					pair = [i,i]

				neg_rules.append(i)
		if pair[0] == pair[1]:
			neg_rules2.append([pair[0]])
		else:
			neg_rules2.append(pair)
		#print("N-"*20)
		#print(neg_rules2)
		#print(neg_rules)


		return {"positives":pos_rules2,"negatives":neg_rules2}








	def calculate_all_correlations_for_a_rule(self,rule1):
		used_rules=self.rules
		correlations =[]
		for i in range(len(used_rules)):

			if rule1.get_id()!= used_rules[i].get_id():
				
				calculate_corr = self.calculate_correlations(rule1,used_rules[i])
				
				if calculate_corr ==1:
					correlations.append(used_rules[i])
		return correlations




	def dfs(self,used_rules,source_file,log_file=None):
		if used_rules==None:
			used_rules=self.rules

		f = open(source_file,"r")

		clusters = []
		visited =set()
		position = -1
		cluster = []
		for line in f:
			print(line)
			if line[0] == "R":
				parts = line.split(" ")
				pair = [int(parts[2]),int(parts[5])]
				print(pair)
				if position != pair[0]:
					if len(cluster)!=0:
						clusters.append(cluster)
					cluster = []
					position = pair[0]
					if (pair[0] not in visited) and (pair[1] not in visited):
						cluster.append(pair[0])
						cluster.append(pair[1])
						visited.add(pair[0])
						visited.add(pair[1])

				else:
					if pair[1] not in visited:
						cluster.append(pair[1])
						visited.add(pair[1])
		#print("clusters:")				
		#print(clusters)

		f.close()
		

		clusters_of_size_1 =0

		average_cluster_size =0



		cluster_number=0

		output_clusters= []
		c_sizes = []
		max_size =-1
		for cluster in clusters:
			#CHECK THIS SPOT
			if len(cluster)==1:
				clusters_of_size_1 +=1
			else:
				print("CLUSTER: #%d" %cluster_number)
				

				average_cluster_size+= len(cluster)
				log_file.write("Cluster C%d"%cluster_number)
				log_file.write("Size: %d"%len(cluster))
				c_sizes.append(len(cluster))
				if max_size<len(cluster):
					max_size = len(cluster)
				log_file.write("Rules:")
				for rule in cluster:
					log_file.write("rule id: %d"%rule)
				log_file.write("\n\n")


				#print(cluster)
				
				intervals = self.calculate_pos_neg_covered(cluster[0])
				#skip cluster that covers nothing
				if intervals["positives"][0][0]==-1 and intervals["negatives"][0][0]==-1:
					continue
				cluster = {"number":cluster_number,"coverage": intervals,"size":len(cluster)}
				cluster_number+=1

				output_clusters.append(cluster)
				print(intervals)
				print("."*20)

				


				log_file.write("Positives:" +str(intervals["positives"]))
				log_file.write("Negatives:" +str(intervals["negatives"]))

		#print(output_clusters)
		#quit()
		possible_sizes =list(range(0,max_size+1))
		#print(possible_sizes)
		#print(c_sizes)
		counters = [0]*len(possible_sizes)

		for ele in c_sizes:
			counters[ele]+=1


		#print(counters)
		
		plt.bar(possible_sizes,counters, color='skyblue', edgecolor='black')

		# Adding labels and title
		plt.xlabel('size')
		plt.ylabel('number of clusters')
		plt.title('Histogram of clusters')
		plt.savefig("plots/histogram.png")
		
		singleton_number=0

		for rule in used_rules:
			singleton_check =True
			for cluster in clusters:
				if rule.get_id() in cluster:
					singleton_check = False

			if singleton_check:
				singleton_number+=1

		#print("singletons: %d"%singleton_number )
		#print(len(used_rules))


		average_cluster_size = average_cluster_size/cluster_number
		
		log_file.write("Average cluster Size: %f"%average_cluster_size)
		log_file.write("Number of singletons: %d"%singleton_number)
		log_file.write("Total number of rules: %d"%len(used_rules))

		quit()
		return output_clusters




	def calculate_diference(self,cluster1,cluster2):
		c1_positives = self.__interval_to_set(cluster1["coverage"]["positives"])
		c1_negatives = self.__interval_to_set(cluster1["coverage"]["negatives"])

		c2_positives = self.__interval_to_set(cluster2["coverage"]["positives"])
		c2_negatives = self.__interval_to_set(cluster2["coverage"]["negatives"])


		positives = c1_positives.symmetric_difference(c2_positives)
		negatives = c1_negatives.symmetric_difference(c2_negatives)

		#print("Calculating difference:")
		#print(cluster1)
		#print(cluster2)
		#print(c1_positives)
		#print(c2_positives)
		#print(positives)
		#print("\n\n")


		if -1 in positives:
			positives.remove(-1)
		if -1 in negatives:
			negatives.remove(-1)


		return(positives,negatives)

	def calculate_intersection(self,cluster1,cluster2):
		c1_positives = self.__interval_to_set(cluster1["coverage"]["positives"])
		c1_negatives = self.__interval_to_set(cluster1["coverage"]["negatives"])

		c2_positives = self.__interval_to_set(cluster2["coverage"]["positives"])
		c2_negatives = self.__interval_to_set(cluster2["coverage"]["negatives"])


		positives = c1_positives.intersection(c2_positives)
		negatives = c1_negatives.intersection(c2_negatives)



		if -1 in positives:
			positives.remove(-1)
		if -1 in negatives:
			negatives.remove(-1)


		return(positives,negatives)


	#Union between 2 clustts
	def calculate_union(self,cluster1,cluster2):
		c1_positives = self.__interval_to_set(cluster1["coverage"]["positives"])
		c1_negatives = self.__interval_to_set(cluster1["coverage"]["negatives"])

		c2_positives = self.__interval_to_set(cluster2["coverage"]["positives"])
		c2_negatives = self.__interval_to_set(cluster2["coverage"]["negatives"])


		positives = c1_positives.union(c2_positives)
		negatives = c1_negatives.union(c2_negatives)



		if -1 in positives:
			positives.remove(-1)
		if -1 in negatives:
			negatives.remove(-1)


		return(positives,negatives)
		


	def calclute_cluster_metrics(self,clusters,log):
		positives_union = set()
		negatives_union =set()


		n_positives = len(self.positives)
		n_negatives = len(self.negatives)

		all_pos_set = set([i for i in range(n_positives)]   )
		all_neg_set = set([i for i in range(n_negatives)]   )

		
	
		positives_intersection =all_pos_set
		negatives_intersection = all_neg_set


		for i in range(len(clusters)):
			positives = self.__interval_to_set(clusters[i]["coverage"]["positives"])
			positives_union=positives_union.union(positives)
			negatives = self.__interval_to_set(clusters[i]["coverage"]["negatives"])
			negatives_union = negatives_union.union(negatives)

	
			if -1 not in positives:
				positives_intersection = positives_intersection.intersection(positives)
			if -1 not in negatives:
				negatives_intersection = negatives_intersection.intersection(negatives)


			

			
			#total_union_positives= total_union_positives.union(set(clusters[i]["coverage"]["positives"])    )
			for j in range(i+1,len(clusters)):
				#print("Diference between C%d and C%d is:"%(i,j))
				#print("C%d size: %d C%d size: %d"%(i,len(clusters[i]["coverage"]["positives"]), j ,len(clusters[j]["coverage"]["positives"])))
				difference =self.calculate_diference(clusters[i],clusters[j])
				if len(difference[0]) ==0:
					log.write("C%d and C%d covers exacly the same positives"%(i,j))
				if len(difference[1]) ==0:
					log.write("C%d and C%d covers exacly the same negatives"%(i,j))
		
		if -1 in positives_union:
			positives_union.remove(-1)
		if -1 in negatives_union:
			negatives_union.remove(-1)

		log.write("Number of positives covered by the combination of the clusters: %d"%len(positives_union))
		log.write("Positives uncatched by the clusters:")
		log.write(str(all_pos_set.symmetric_difference(positives_union)))


		log.write("Number of negatives covered by the combination of the clusters: %d"%len(negatives_union))
		log.write("Negatives uncatched by the clusters:")
		log.write(str(all_neg_set.symmetric_difference(negatives_union)))

		log.write("Intersection of all positives:")
		log.write(str(positives_intersection))
		log.write("Intersection of all negatives:")
		log.write(str(negatives_intersection))







	def creat_upsetplot(self,sets_data,title,size):
		print(sets_data)
		#quit()

		# First, get all unique elements across all sets
		all_elements = sorted(list(set().union(*sets_data.values())))

		# Create a boolean DataFrame indicating membership for each element in each set

		membership_df = pd.DataFrame({
			name: [element in s for element in all_elements]
			for name, s in sets_data.items()
		}, index=all_elements)

		# Convert to the expected Series format for upsetplot
		# The index should be a MultiIndex where each level is a set name and the value is True if the element is in the set.
		# This specific transformation is sometimes tricky. Let's create a simpler one for illustration.

		# A more direct way to prepare data for upsetplot:
		# Create a list of Series where the index indicates set membership and values are 1 (or count).
		# For basic presence, we can use a binary matrix directly.

		# Let's try to directly use the membership_df after dropping elements not belonging to any set (optional)
		# Or, even better, prepare a Series with a MultiIndex directly from the sets.

		from itertools import combinations
		from collections import defaultdict
		
		# A helper function to get the intersection counts
		def get_intersection_counts(sets_dict):
			elements_to_sets = defaultdict(list)
			for set_name, s in sets_dict.items():
				for element in s:
					elements_to_sets[element].append(set_name)

			# Create a MultiIndex Series
			# Each index represents an element, and its levels indicate which sets it belongs to.
			# The values in the Series will be 1 (representing a count of 1 for that element).
			upset_data = []
			for element, member_of_sets in elements_to_sets.items():
				# Sort the set names to ensure consistent indexing
				member_of_sets.sort()
				upset_data.append((tuple(member_of_sets), 1))

			# Create a Series with a MultiIndex
			# The index names should match the set names if possible, but upsetplot handles boolean Series as well.
			# For this, we need to create a Series where the index is a boolean mask for each element indicating membership.
			
			# A simpler way to get a Series for upsetplot is to use from_memberships
			from upsetplot import from_memberships

			# Create a list of lists where each inner list contains the set names an element belongs to
			memberships_list = []
			for element, member_of_sets in elements_to_sets.items():
				memberships_list.append(member_of_sets)


			# Create the Series compatible with upsetplot
			# Fix: Provide 'data' as a list of ones with the same length as 'memberships_list'
			upset_series = from_memberships(memberships_list, data=[1] * len(memberships_list))


			# Aggregate by the index to sum counts for identical intersection groups, making the index unique
			if not upset_series.index.is_unique:
				upset_series = upset_series.groupby(level=list(range(upset_series.index.nlevels))).sum()
			
			return upset_series

		# Get the upset_series
		upset_series = get_intersection_counts(sets_data)

		# Plot the UpSet plot
		fig = plt.figure(figsize=(10, 6))
		plot(upset_series, fig=fig, show_counts=True)
		plt.suptitle(title)
	    
		plt.savefig("plots/"+title+".png")
		plt.close()






	def find_veen(self,clusters):
		new_clusters =[]

		for cluster in clusters:
			cluster_v = {
			"number": cluster["number"],
			"positives": self.__interval_to_set(cluster["coverage"]["positives"]),
			"negatives": self.__interval_to_set(cluster["coverage"]["negatives"]),
			"size": cluster["size"]
			}
			new_clusters.append(cluster_v)

		new_clusters = sorted(new_clusters, key=lambda x: x["size"])


		sizes_v = [c["size"] for c in new_clusters]
		sizes_v =sorted(list(set(sizes_v)))

		sized_sets = {}
		for size in sizes_v:
			sized_sets[size] = []



		for i in range(len(new_clusters)):
			sized_sets[new_clusters[i]["size"]].append(i) 






		for size in sizes_v:
			number_clusters  = len(sized_sets[size])
			

			
				
			positive_sets = {}
			for cluster2 in sized_sets[size]:
				#print("-"*20)
				#print(new_clusters[cluster2])
				
				if -1 not in new_clusters[cluster2]["positives"]:
					positive_sets["Set"+str(new_clusters[cluster2]["number"])] = new_clusters[cluster2]["positives"]
					


			if number_clusters >=2 and number_clusters <= 6:
				
				fig, ax = plt.subplots(figsize=(10, 10))

				# Generate the 4-set Venn diagram
				venn(positive_sets, ax=ax)

				# Add the title to the plot
				plt.title(str(size)+"veen positives")
					

				plt.savefig("plots/"+str(size)+"veenPositives.png")
				plt.close()
			elif number_clusters > 6:
				self.creat_upsetplot(positive_sets,"subsets of size " + str(size)+"UpSet Plot positives",size)


		for size in sizes_v:
			number_clusters  = len(sized_sets[size])

			negative_sets = {}
			
				
				
			for cluster2 in sized_sets[size]:
				#print("-"*20)
				#print(new_clusters[cluster2])
				negative_sets["Set"+str(new_clusters[cluster2]["number"])] = new_clusters[cluster2]["negatives"]
				



				
			if number_clusters >=2 and number_clusters <= 6:
				fig, ax = plt.subplots(figsize=(10, 10))

				# Generate the 4-set Venn diagram
				venn(negative_sets, ax=ax)

				# Add the title to the plot
				plt.title(str(size)+"veen negatives")
					

				plt.savefig("plots/"+str(size)+"veenNegatives.png")
				plt.close()
			elif number_clusters > 6:
				self.creat_upsetplot(negative_sets,"subsets of size " + str(size)+"UpSet Plot negatives",size)


		


	#private


	def __interval_to_set(self,interval):
		new_list = []

		for elem in interval:
			
			if len(elem)==1:
				new_list.append(elem[0])
			else:
				for i in range(elem[0],elem[1]+1):
					new_list.append(i)
		return set(new_list)






	#rule length utilities


	#for a certain rule checks how many rules in a given list are childs of tha rule
	#a rule A is a child of a rule B if the head of the rules are the same and the rule A have a length superior to B and a common prefix on the body
	def __calculate_degree_of_rule(self,rule,rule_list):
		count =0
		for r in rule_list:
			if r.is_subrule(rule) and not (r.get_id()== rule.get_id()):
				count+=1
		return count


	#calculate metric

	#calculates a given score for a list of rules if no list is provided it uses all rules in the data
	# return list of pairs (int,float) corresponding the id of a rule represented by a interger and that rule score evaluation to each rule
	def __calculate_score(self,score,rules=None):
		if rules==None:
			return [ (rule,score.calculate(rule,self.__coverage[rule.get_id()] )) for rule in self.rules]
		return [ (rule,score.calculate(rule,self.__coverage[rule.get_id()] )) for rule in rules]

	#receives a list of scores [(int,float)] -> [(rule id,score evaluated)] and extracts a single list of all scores evaluated
	#was made to allow calculation of mean, medians over the results of a score 
	def __extract_values_of_score_list(self,scores):
		return [score[1] for score in scores]



	#processes the rules that came from aleph
	def __dettach_rules_from_other_info(self):
		tmp_rules = []

		
		#A rule on that point is a dictionary with the following keys
		#
		# head: a string that represents the head of a rule
		# tail: a list of strings representing the body of the rule
		# positives: A list of positives a dictionary {name,content} where name is the key for the name of the literal and content are the two variables of 
		# 	the literal, those positives are covered by the rule.
		# negatives: equivalent to the positives but now is a list of the negative coverage instead

		for rule in self.rules:
			print("Processing Rule: %s :- %s\n" % (rule["head"],rule["tail"]))
			#Converting the head of the rule in a literal to simplicity
			lit= rule["head"]
			head_processed = Literal(lit)
		

			#Each element of the body will also be a new literal
			body = [ Literal(lit) for lit in rule["tail"]]

			#Usint the head, and the body converted in literal we will constructed a new rule
			rule_instance = Rule(self.__rule_id,head_processed,body)
			

			tmp_rules.append(rule_instance)
			
			
			#Now we process the true positives and true negatives from aleph
			true_positives_aleph = [Literal(lit) for lit in rule["positives"] ]

			true_negatives_aleph = [Literal(lit) for lit in rule["negatives"] ]
			





			#Make sure the rules that covers a certain example are associated with the them in a (example->rule id) relationship 


			#for each positive we save whose rules are covering it
			for pos in true_positives_aleph:
				self.__rule_positives.add(pos,self.__rule_id)

			for neg in true_negatives_aleph:
				self.__rule_negatives.add(neg,self.__rule_id)




			#After this step if we want to know what rules coves the positives with index 1 we can do self.__rule_positives[ self.positives[i] ]

			#coverage with the maximun number of positives and negatives on the dataset. The true positives and negatives can be extracted from aleph. 
			number_of_positives = len(true_positives_aleph)
			number_of_negatives = len(true_negatives_aleph)


			#print(f"Rule: {rule}")
			#print(true_positives_aleph)

			


			coverage_instance = Coverage(len(self.positives), len(self.negatives),positive=number_of_positives,negative=number_of_negatives)
			#quit()
			#we add associate the coverage we instanciate with the rule id we are working with
			self.__coverage[self.__rule_id] = coverage_instance

			self.__rule_id +=1


			
		self.rules = tmp_rules




	#create plots and stat_logs logs folders to save results
	def __set_working_enviorment(self):
		
		#Generate paths for plots and stats_logs using the actual path as prefix
		plot_path =  self.__get_file_path("plots")
		logs_path =  self.__get_file_path("stat_logs")

		#create the folders if the the file didn't existed yet
		if not os.path.isdir(plot_path) and not os.path.exists(plot_path) :
			os.mkdir(plot_path)
		if not os.path.isdir(logs_path) and not os.path.exists(logs_path) :
			os.mkdir(logs_path)


	#utility to generate and return a path using a file name and the actual absolute path as prefix
	def __get_file_path(self,file):
		#get absolute path of the actual folder 
		absolute_path = os.path.abspath(os.getcwd())
		return os.path.join(absolute_path, file)



















''' OLD UNUSING code

	#Coverage functions
	def __calculate_coverage(self):
		print("Calculating positives coverage...")
		start = time.time()
		self.__calculate_positive_coverage()
		end = time.time()
		print(end - start)
		print("Calculating negative coverage...")
		start = time.time()
		self.__calculate_negative_coverage()
		end = time.time()
		print(end - start)



	def __calculate_negative_coverage2(self):
		for rule in self.rules:
			coverage =0
			#TODO:ordenar negativos em ambos os casos
			for i in range(len(self.negatives)):  #n
				rule_id = self.__rule_negatives[self.negatives[i]]
				self.neg_rule[i].append(rule_id)
				coverage +=1
					
			self.__coverage[rule.get_id()].set_negatives(coverage)


	def __calculate_negative_coverage(self):
		#id_negativo -> id rule
		for i in range(len(self.negatives)):
			rule_ids= self.__rule_negatives.get_rule_ids(self.negatives[i])
			for rule_id in rule_ids:
				self.neg_rule[i].append(rule_id) 
				actual_negatives = self.__coverage[rule_id].get_negative()
				self.__coverage[rule_id].set_negatives(actual_negatives+1)



	def __calculate_positive_coverage(self):
	
		#unnecessary lets analize
		for i in range(len(self.positives)):
			rule_ids= self.__rule_positives.get_rule_ids(self.positives[i]) #extracting ids from self.__rule_positives {str(positive)->rule_id}
			for rule_id in rule_ids:
				self.pos_rule[i].append(rule_id) #create a list of positive_id -> rule_ids unnecesary wer already have that information
				actual_positives = self.__coverage[rule_id].get_positive()
				self.__coverage[rule_id].set_positives(actual_positives+1)
				


					
			
'''