import gensim
import nltk
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from os import listdir
from os.path import isfile, join
tokenizer = RegexpTokenizer(r"\w+")
from nltk import word_tokenize, pos_tag
import sys

from math import ceil, floor
def float_round(num, places = 0, direction = floor):
    return direction(num * (10**places)) / float(10**places)


filename=sys.argv[1]
# nltk.download('stopwords')
# tokenizer = RegexpTokenizer(r'\w+')
stopword_set = set(stopwords.words('english'))
inputp=open("clean_data/"+filename+".csv","r")

data=[]

for line in inputp.readlines():
	data.append(line.strip())
# print data
inputp.close()

def loadGloveModel(gloveFile):
    # print "Loading Glove Model"
    f = open("glove/glove.6B/glove.6B.200d.txt",'r')
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = [float(val) for val in splitLine[1:]]
        model[word] = embedding
    print "Hi how may I help you"
    return model


def determine_tense_input(sentance):
    text = word_tokenize(sentance)
    tagged = pos_tag(text)

    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ","VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]]) 
    return(tense)


def nlp_clean(data):
	new_data = []
	for d in data:
		if "," in d:
			new_str = d.lower().split(",")[1]
		else:
			new_str = d.lower()
		dlist = tokenizer.tokenize(new_str)
		dlist = list(set(dlist).difference(stopword_set))
		if "," in d:
			dlist.append(d.lower().split(",")[0])
		else:
			dlist.append("rep")
		new_data.append(dlist)
	return new_data

clean_data= nlp_clean(data)

d2v_model = gensim.models.doc2vec.Doc2Vec.load('doc2vec3.model')

inputp=open("clean_data/"+filename+".csv","r")

filevecnegs=open("vectors/negs_vec","w")
filevecpos=open("vectors/pos_vec","w")

for i,origline in zip(clean_data,inputp.readlines()):
	inferred_embedding = d2v_model.infer_vector(i[:-1])
	line=""
	count=2
	for vec in inferred_embedding:
		line=line+" "+str(count)+":"+str(vec)
		count+=1
	if i[len(i)-1]=="rep":
		line=line+" "+str(count)+":"+"1"
	else:
		line=line+" "+str(count)+":"+"0"
	
	count+=1

	if "," in origline:
		stats=determine_tense_input(origline.strip().split(",")[1])
	else:
		stats=determine_tense_input(origline)

	if filename=="pos":
		for l,z in stats.iteritems():
			line+=" "+str(count)+":"+str(z)
			count+=1
		filevecpos.write("1 "+line.strip()+" "+str(count)+":"+str(len(origline.split(" ")))+"\n")
		# print "1 "+line.strip()+" "+str(count)+":"+str(len(origline.split(" ")))


	else:
		for l,z in stats.iteritems():
			line+=" "+str(count)+":"+str(z)
			count+=1
		filevecnegs.write("2 "+line.strip()+" "+str(count)+":"+str(len(origline.split(" ")))+"\n")
		# print "2 "+line.strip()+" "+str(count)+":"+str(len(origline.split(" ")))

filevecpos.close()
filevecnegs.close()


