from literals import Literal


class Rule:
	def __init__(self,rule_id,head,body):
		self.__rule_id =rule_id
		self.__head = head
		self.__body = body

	def get_id(self):
		return self.__rule_id

	def get_head(self):
		return self.__head

	def get_body(self):
		return self.__body

	def is_subrule(self,target):
		if len(target.get_body())<=len(self.__body):
			return False
		if target.get_head() != self.__head:
			return False

		is_equal = True

		for i in range(len(self.__body)):
			if self.__body[i].get_name() != target.get_body()[i].get_name():
				is_equal=False
				break
		return is_equal




	def length(self):
		return len(self.__body)

	def kaur_format(self):
		body = ", ".join([str(lit).replace("twin","_") for lit in self.__body])

		return "(" +" :-  ".join([str(self.__head).replace("(A,B)","(A,B,0)"),body]) +", !)."

	def __str__(self):
		body = ", ".join([str(lit) for lit in self.__body])

		return ": ".join([str(self.__head),body])

	def __repr__(self):
		return str(self)



	def same_rule(self,other_rule,equivalences=None):
		if self.length() != other_rule.length():
			return False

		is_equal = True

		for i in range(len(self.__body)):
			
			if self.__body[i].get_name() != other_rule.get_body()[i].get_name():
				if equivalences!= None :
					if (self.__body[i].get_name() not in equivalences.keys()) or (other_rule.get_body()[i].get_name() not in equivalences.keys()):
						is_equal=False
						break

					print(self.__body[i].get_name())
					print(other_rule.get_body()[i].get_name())
					print("-"*20)
					equivalence1 = equivalences[self.__body[i].get_name()] == other_rule.get_body()[i].get_name()
					equivalence2 = self.__body[i].get_name() == equivalences[other_rule.get_body()[i].get_name()]
					if not equivalence1 and not equivalence2:
						is_equal=False
						break
				else:
					is_equal=False
					break
		return is_equal

