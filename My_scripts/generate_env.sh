#!/bin/bash
# program $number_of_folders $learning_target $dataset_name 
# dataset should be a folder in ~/NNRPT

re='^[0-9]+$'


if ! [[ "$1" =~ ^[0-9]+$ ]] ; then
	echo "ERROR: first parameter should be an interger"
	exit 1

fi

#Create initial directory
mkdir 1

#Create Test pat
mkdir 1/Test
mkdir 1/Test/test
mkdir 1/Test/train
mkdir 1/Test/train/models
mkdir 1/Test/train/models/bRDNs
mkdir 1/Test/train/models/bRDNs/Trees

#Create Training path
mkdir 1/Training
mkdir 1/Training/test
mkdir 1/Training/train
mkdir 1/Training/train/models
mkdir 1/Training/train/models/bRDNs
mkdir 1/Training/train/models/bRDNs/Trees


#make common symbolic links

ln -s ~/NNRPT/$3/Test/imdb_bk.txt ./1/Test/imdb_bk.txt
ln -s ~/NNRPT/$3/Test/test/test_bk.txt ./1/Test/test/test_bk.txt 
ln -s ~/NNRPT/$3/Test/test/test_facts.txt ./1/Test/test/test_facts.txt
ln -s ~/NNRPT/$3/Test/test/test_null.txt ./1/Test/test/test_null.txt
ln -s ~/NNRPT/$3/Test/train/models/bRDNs/$2.model ./1/Test/train/models/bRDNs/$2.model 


current_dir=$(pwd)
ln -s $current_dir/examples_data/Test/test_neg.txt ./1/Test/test/test_neg.txt 
ln -s $current_dir/examples_data/Test/test_pos.txt ./1/Test/test/test_pos.txt 



#Training
ln -s ~/NNRPT/$3/Training/imdb_bk.txt ./1/Training/imdb_bk.txt
ln -s ~/NNRPT/$3/Training/test/test_bk.txt ./1/Training/test/test_bk.txt 
ln -s ~/NNRPT/$3/Training/test/test_facts.txt ./1/Training/test/test_facts.txt
ln -s ~/NNRPT/$3/Training/test/test_null.txt ./1/Training/test/test_null.txt
ln -s ~/NNRPT/$3/Training/train/models/bRDNs/$2.model ./1/Training/train/models/bRDNs/$2.model 

ln -s $current_dir/examples_data/Training/test_neg.txt ./1/Training/test/test_neg.txt 
ln -s $current_dir/examples_data/Training/test_pos.txt ./1/Training/test/test_pos.txt 


for i in `seq 2 $1`
do
	cp -R 1 $i
done

targets_path=$current_dir/../Targets

for i in `seq 1 $1`
do
	ln -s $targets_path/T$i ./$i/Test/train/models/bRDNs/Trees/$2Tree0.tree 
	ln -s $targets_path/T$i ./$i/Training/train/models/bRDNs/Trees/$2Tree0.tree 
done

#Make symbolic links for the positives and negatives