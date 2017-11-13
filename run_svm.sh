shuf vectors/negs_vec | head -550 > vectors/temp_negs
head -50 vectors/temp_negs > vectors/test_negs
tail -400 vectors/temp_negs > vectors/train_data
shuf vectors/pos_vec  > vectors/temp_pos
head -20 vectors/temp_pos > vectors/test_pos
tail -200 vectors/temp_pos >>vectors/train_data
cat vectors/test_pos vectors/temp_negs > vectors/test_acc
# rm temp_negs
# rm temp_pos
echo "-----------------------training started---------------------------------------------------"
svm_multiclass_linux64/svm_multiclass_learn -c 200 -t 2 -d 1 vectors/train_data model_train_data 
echo "-----------------------training completed---------------------------------------------------"
echo "-----------------------testing---------------------------------------------------"
svm_multiclass_linux64/svm_multiclass_classify vectors/test_pos model_train_data out | tail -1
svm_multiclass_linux64/svm_multiclass_classify vectors/test_negs model_train_data out | tail -1



