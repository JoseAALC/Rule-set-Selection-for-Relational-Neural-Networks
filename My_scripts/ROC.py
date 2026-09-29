

TOTAL = 126
pred_f = open("Predictions.txt","r")


predictions =[]
Y = []
for l in pred_f:
	parts = l.strip().replace("Y:","").split(" ")

	pred1 = float(parts[0])
	pred2 = float(parts[1])
	predictions.append([pred1,pred2])
	Y.append([float(parts[2]),float(parts[3])])

TP=[]
FN=[]
FP =[]
TN =[]

TPR =[]
TNR =[]
#let 0,1 be postive
step =0
pos=0

Remaining = TOTAL - len(predictions)
while step <=1:
	TP.append(0)
	FN.append(0)
	FP.append(0)
	TN.append(0)
	TPR.append(0)
	TNR.append(0)
	for i in range(len(predictions)):
		if Y[i][1]==1 and predictions[i][1]>=step: 
			TP[pos]+=1
		if Y[i][1]==1 and predictions[i][1] < step:
			FN[pos]+=1
		if Y[i][0]==1 and predictions[i][0] >= step:
			TN[pos]+=1
		if Y[i][0]==1 and predictions[i][0] < step:
			FP[pos]+=1

	if TP[pos] + FN[pos] +Remaining >0:
		TPR[pos]=TP[pos]/ (TP[pos] + FN[pos] +Remaining)
	else:
		TPR[pos] =0
	if TN[pos] + FP[pos] +Remaining>0:

		TNR[pos]=TN[pos]/ (TN[pos] + FP[pos] +Remaining)

	else: 
		TNR[pos]=0





	step+=0.1
	pos+=1
print(TPR)
print(TNR)
pred_f.close()