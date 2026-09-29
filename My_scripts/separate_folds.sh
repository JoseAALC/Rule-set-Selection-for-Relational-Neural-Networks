#!/bin/bash

cat neg_fold2.txt neg_fold3.txt neg_fold4.txt neg_fold5.txt > fold1/train_neg.txt
cp neg_fold1.txt fold1/test_neg.txt

cat neg_fold1.txt neg_fold3.txt neg_fold4.txt neg_fold5.txt > fold2/train_neg.txt
cp neg_fold2.txt fold2/test_neg.txt

cat neg_fold1.txt neg_fold2.txt neg_fold4.txt neg_fold5.txt > fold3/train_neg.txt
cp neg_fold3.txt fold3/test_neg.txt

cat neg_fold1.txt neg_fold2.txt neg_fold3.txt neg_fold5.txt > fold4/train_neg.txt
cp neg_fold4.txt fold4/test_neg.txt

cat neg_fold1.txt neg_fold2.txt neg_fold3.txt neg_fold4.txt > fold5/train_neg.txt
cp neg_fold5.txt fold5/test_neg.txt

cat pos_fold2.txt pos_fold3.txt pos_fold4.txt pos_fold5.txt > fold1/train_pos.txt
cp pos_fold1.txt fold1/test_pos.txt

cat pos_fold1.txt pos_fold3.txt pos_fold4.txt pos_fold5.txt > fold2/train_pos.txt
cp pos_fold2.txt fold2/test_pos.txt

cat pos_fold1.txt pos_fold2.txt pos_fold4.txt pos_fold5.txt > fold3/train_pos.txt
cp pos_fold3.txt fold3/test_pos.txt

cat pos_fold1.txt pos_fold2.txt pos_fold3.txt pos_fold5.txt > fold4/train_pos.txt
cp pos_fold4.txt fold4/test_pos.txt

cat pos_fold1.txt pos_fold2.txt pos_fold3.txt pos_fold4.txt > fold5/train_pos.txt
cp pos_fold5.txt fold5/test_pos.txt