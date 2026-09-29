import os

class Logger:

	def __init__(self,file=None):
		self.file = file
		self.defaut_dir = os.path.join(os.path.abspath(os.getcwd()),"stat_logs") 

		self.writter =None

		if file!=None:
			total_file = os.path.join(self.defaut_dir ,self.file)
			self.writter = open(total_file,"w")

	def write(self,string):
		if self.writter !=None: 
			self.writter.write(string + "\n")
		else:
			print(string)

	def __del__(self):
		if self.writter !=None: 
			self.writter.close()
			print("File: %s closed" %self.file)
