#!/bin/bash
datafile="datare.txt"
tmpfile="tmpfile.tmp"
logfile=$1"_logfile.log"
nrecs=10
minusers=500
knn=210
nsvd=4
mmm="mean"

echo "Parameters:" $1 > $logfile
echo $1 | bash parse.sh 2>> $logfile | python reformat.py > $tmpfile
python model_knn_predict.py $nsvd $tmpfile $minusers $knn $mmm $nrecs < $datafile 2>>$logfile | bash getnamefromlist.sh 2>>$logfile