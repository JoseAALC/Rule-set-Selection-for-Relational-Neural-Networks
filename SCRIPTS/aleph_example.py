


class Aleph_Example:

	def __init__(self,examples):
		self.example_id_dic = {}

		for example in examples:
			self.example_id_dic[example]=[]


	def add(self,example,rule_id):
		if not example in self.example_id_dic:
			raise Exception("Trying to add element to the key:%s where that key don't exists"%example)
		self.example_id_dic[example].append(rule_id)

	def get_rule_ids(self,example):
		return self.example_id_dic[example]

