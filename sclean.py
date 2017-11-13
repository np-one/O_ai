import json

filename=sys.argv[1]
outpos=open("cleandata/pos.csv","w")
outnegs=open("cleandata/negs.csv","w")

set_1=set()
with open('data') as f:
    data = f.read()
    points=data.split("\n\n")
    leng=len(points)
    count=0
    for i in points:
    	count+=1
    	if count==leng:
    		continue
    	jsondata = json.loads(i)
    	data1= jsondata["transcription_merged"]
    	for p1 in data1:
    		flag=False
    		vline=""
    		if "speaker" in p1:
    			vline+=str(p1["speaker"].encode('utf-8')).replace("\,","")+","
    		else:
    			vline+=","	

    		if 'line' in p1:
    			vline+=str(p1["line"].encode('utf-8')).replace("\,","").replace(",","")+","
    		else:
    			vline+=","	

    		if 'segment' in p1:
    			if str(p1["segment"].encode('utf-8'))=="Next steps and action items":
    				flag=True
    		if flag:
                outpos.write(vline+"\n")
            else:
                outnegs.write(vline+"\n")
outpos.close()
outnegs.close()
