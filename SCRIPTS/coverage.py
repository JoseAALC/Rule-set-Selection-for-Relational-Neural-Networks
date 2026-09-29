



class Coverage:


	def __init__(self,total_pos,total_neg,positive=0,negative=0):
		self.__positive =positive
		

		self.FP =negative
		self.FN =0
		self.__negative =0

		self.__total_pos = total_pos
		self.__total_neg = total_neg

		self.__pre_calculate_FN_FP()

	#getters
	def get_positive(self):
		return self.__positive

	def get_negative(self):
		return self.__negative

	def get_total_positives(self):
		return self.__total_pos

	def get_total_negatives(self):
		return self.__total_neg

	#setters

	def set_positives(self,positives):
		self.__positive = positives
		self.__pre_calculate_FN_FP()

	def set_negatives(self,negatives):
		self.__negative = negatives
		self.__pre_calculate_FN_FP()


	def get_TP(self):
		return self.__positive 
	
	def get_TN(self):
		return self.__negative 

	def get_FN(self):
		return self.FN

	def get_FP(self):
		return self.FP 

	def __pre_calculate_FN_FP(self):



		#rule_list[r]["FP"] = len(negatives)- rule_list[r]["negative_c"]
		#rule_list[r]["FN"] = len(positives)-rule_list[r]["positive_c"] 
		self.__negative = self.__total_neg - self.FP
		#self.FP = self.__total_neg - self.get_TN()  
		self.FN = self.__total_pos -self.get_TP()



	def __str__(self):
		return "Positive: " + str(self.__positive) + " Negative: " +str(self.FP)

	def __repr__(self):
		return str(self)