


#TRAIN examples
f = open("TrainOutputRW.txt","r")

train_examples =set()
for l in f:

	head = l.split(" :- ")[0].strip()
	head = head[1:-1]
	head = head.split("(")[1].strip().replace(" ","")
	train_examples.add(head)
	



f.close()

print(len(train_examples))


#Test examples

f = open("TestOutputRW.txt","r")

test_examples =set()
for l in f:

	head = l.split(" :- ")[0].strip()
	head = head[1:-1]
	head = head.split("(")[1].strip().replace(" ","")
	test_examples.add(head)
	



f.close()

print(len(test_examples))