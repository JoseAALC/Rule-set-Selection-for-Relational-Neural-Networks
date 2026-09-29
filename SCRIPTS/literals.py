

class Literal:
	def __init__(self,text_literal):

		if isinstance(text_literal,str):
			self.__string_resolve(text_literal)
		elif isinstance(text_literal,dict) and ("name" in text_literal ) and ("content" in text_literal): 
			self.__name_arguments_resolve(text_literal["name"],text_literal["content"])
			

		return;

	def get_name(self):
		return self.__name

	def get_first(self):
		return self.__first

	def get_second(self):
		return self.__second

	
	def __string_resolve(self,literal):
		text = literal.strip()
		text_parts = text.replace("(",",").replace(")","").strip().split(",")
		self.__name = text_parts[0]
		self.__first = text_parts[1].replace("\"","")
		self.__second = text_parts[2].replace("\"","")

	def __name_arguments_resolve(self,name,arguments):

		self.__name = name.strip()
		self.__first = arguments[0].strip().replace("\"","")
		self.__second = arguments[1].strip().replace("\"","")

	def __str__(self):
		return "".join([self.__name,"(",self.__first, "," + self.__second,")"])

	def __repr__(self):
		return str(self)

	def __eq__(self,other):
		if isinstance(other,Literal):
			name_eq = (self.__name == other.get_name())
			firs_eq = (self.__first == other.get_first())
			second_eq = (self.__second== other.get_second())
			return name_eq and firs_eq and second_eq
		return False

	def __hash__(self):
		return hash(self.__str__())




		