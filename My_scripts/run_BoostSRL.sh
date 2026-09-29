#!/bin/bash
# $1 =working folder
# $2 = perdiction target

java -Xmx62g -jar GroundedRandomWalks.jar -grw -mln -trees 1 -i -test $1/Training/test/ -target $2 -model $1/Training/train/models/ -aucJarPath ./ 
java -Xmx62g -jar GroundedRandomWalks.jar -grw -mln -trees 1 -i -test $1/Test/test/ -target $2 -model $1/Test/train/models/ -aucJarPath ./ 
