#!/bin/bash
rm $1"_errors"
echo "Getting Errors for "$1" Eigenvalues"
for i in {0..9}
do
    echo $i"-th Subsample"
    python model_knn.py $1 $i"_tvalidation_re" $i"_vvalidation_re" 75 mean < $i"_training_re" >> $1"_errors"
done