import json
from glob import glob

def addloc(data,lang,loc):
    pass
for x in glob("*.json"):
    print(x)
    with open(x, "r+",encoding='utf-8') as f:
        data = json.load(f)
        for tweet in data:
            if(tweet['city']=='NYC'):
                tweet['city']="nyc"
            elif(tweet['city']=='Mexico City'):
                tweet['city']="mexico city"
            elif(tweet['city']=='mexio city'):
                tweet['city']="mexico city"
            elif(tweet['city']=='mexico'):
                tweet['city']="mexico city"
            elif(tweet['city']=='Bangkok'):
                tweet['city']="bangkok"
            elif(tweet['city']=='Paris'):
                tweet['city']="paris"
            elif(tweet['city']=='Delhi'):
                tweet['city']="delhi"
    with open(x, 'w') as outfile: 
        json.dump(data, outfile, sort_keys=True, indent=4)
