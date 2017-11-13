import gensim
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, join


docLabels = []
docLabels = [f for f in listdir("data_all")]

data = []
for doc in docLabels:
	f=open("data_all/" + doc, "r")
	data.append(f.read())
	f.close()
	# print doc
tokenizer = RegexpTokenizer(r"\w+")
# nltk.download('stopwords')
# tokenizer = RegexpTokenizer(r'\w+')
stopword_set = set(stopwords.words('english'))

#This function does all cleaning of data using two objects above

def nlp_clean(data):
   new_data = []
   for d in data:
      new_str = d.lower()
      dlist = tokenizer.tokenize(new_str)
      dlist = list(set(dlist).difference(stopword_set))
      new_data.append(dlist)
   return new_data


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):

        self.labels_list = labels_list
        self.doc_list = doc_list

    def __iter__(self):

        for idx, doc in enumerate(self.doc_list):
              yield gensim.models.doc2vec.LabeledSentence(doc,    
[self.labels_list[idx]])

# print data
data = nlp_clean(data)  
it = LabeledLineSentence(data, docLabels)            


model = gensim.models.Doc2Vec(size=300, min_count=5, alpha=0.025, min_alpha=0.025)
model.build_vocab(it)

#training of model
for epoch in range(100):
 print "iteration "+str(epoch+1)
 model.train(it,total_examples=model.corpus_count, epochs=model.iter)
 model.alpha -= 0.002
 model.min_alpha = model.alpha
 model.train(it,total_examples=model.corpus_count, epochs=model.iter)
model.save("doc2vec3.model") 
print "model saved"

