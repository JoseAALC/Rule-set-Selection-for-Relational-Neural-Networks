
from coverage import Coverage


class Score:
	def calculate(self, rule,coverage):
		return 0


#Number of positives - number of negatives
class Score_1(Score):
	def calculate(self, rule,coverage):
		return coverage.get_TP()-coverage.get_TN()


class Score_2(Score):
	def calculate(self, rule,coverage):
		return coverage.get_TN()-coverage.get_TP()

class Precision(Score):
	def calculate(self, rule,coverage):
		tp = coverage.get_TP()
		if tp + coverage.get_FP()==0:
			return 0
		return tp/(tp + coverage.get_FP())

class Recall(Score):
	def calculate(self, rule,coverage):

		tp = coverage.get_TP()

		#print("TP: %f, FN: %f" % (tp,coverage.get_FN()))
		if tp + coverage.get_FN() ==0:
			return 0
		return tp/(tp + coverage.get_FN())

class F1(Score):
	def calculate(self, rule,coverage):
		recall = Recall()
		precision = Precision()
		
		recall_score = recall.calculate(rule,coverage)
		presision_score = precision.calculate(rule,coverage)

		if presision_score+recall_score ==0:
			return 0
		score = 2* recall_score*presision_score/(presision_score+recall_score)
		return score


class Positivec(Score):
	def calculate(self, rule,coverage):
		return coverage.get_TP()/coverage.get_total_positives()

class Negativec(Score):
	def calculate(self, rule,coverage):
		return coverage.get_FP()/coverage.get_total_negatives()



class Percentages(Score):
	def calculate(self, rule,coverage):
		positive_rate= coverage.get_TP()/coverage.get_total_positives()
		negative_rate= coverage.get_FP()/coverage.get_total_negatives() 
		return positive_rate- negative_rate







#Define latet this scores

def f1(rule):
	recall_score = recall(rule)
	presision_score = presision(rule)
	if presision_score+recall_score ==0:
		return 0
	score = 2* recall_score*presision_score/(presision_score+recall_score)
	return score


def antipresision(rule):
	tp = rule["negative_c"]
	if tp+ rule["AFP"] ==0:
		return 0
	return tp/(tp+ rule["AFP"])


def antirecall(rule):
	tp = rule["negative_c"]
	if tp + rule["AFN"]:
		return 0
	return tp/(tp + rule["AFN"])


def antif1(rule):
	recall_score = antirecall(rule)
	presision_score = antipresision(rule)
	if presision_score+recall_score ==0:
		return 0
	score = 2 *recall_score*presision_score/(presision_score+recall_score)
	return score








print(issubclass(type(F1()),Score))