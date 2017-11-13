# O_ai

Problem:
Classify the dialog as "Next step" type or "Not Next step".

Libraries Used:
1. Gensim 3.1: Doc2vec
2. NLTK NLP: Preprocess Text
3. MultiClass SVM: Train Classifier

Solution:
1.  Preprocess:
     *   NLP tokenize. (NLTK)
     *   Stop Words Removal.
2.  Trained a Doc2vec model on the whole corpus (200+15000). (GENSIM)
3.  Coverted each line into a 300 D vector using above.
4.  Added features
     *   Distribution of tense in verbs (Most of the positive examples refer to future tense / Next steps).
     *   Boolean feature Speaker of line(Prospect / Rep).
     *   Time of the call(End time- Start time). (Because very short and very long calls are mostly negative examples).
5.  Used MultiClass SVM Library to train with all positive examples and downsampled negative examples.

Steps to Run:
1. Run sclean.py to read json data and create csv files.
2. Run gensim_test.py to create doc2vec model.
3. Run prepare_vectors.py for creating vectors of data from prepared doc2vec.
4. Run run.sh to train and test svm on the prepared data.
