#!/bin/bash
# program $number_of_folders 


#TEST
cat ./1/Test/test/OutputRW.txt >testOutputRW.txt


for i in `seq 1 $1`
do
	cat  ./$i/Test/test/OutputRW.txt >> testOutputRW.txt
done

#TRAIN


cat ./1/Training/test/OutputRW.txt >trainOutputRW.txt


for i in `seq 1 $1`
do
	cat ./$i/Training/test/OutputRW.txt >> trainOutputRW.txt
done