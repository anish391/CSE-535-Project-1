import json
import random
import time
from glob import glob

arr = ["en","es","th","hi","fr"]
arr1=[]
count = 0
for x in glob("*.json"):
    with open(x) as file:
        print(x)
        data = json.load(file)
        count = 0
        for i in data:
            tweet_date=time.strftime('%Y-%m-%dT%H:00:00Z', time.strptime(i["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
            i["tweet_date"] = tweet_date
    with open(x, 'w') as outfile:  
        json.dump(data, outfile, sort_keys=True, indent=4)


"""
tweet_date=time.strftime('%Y-%m-%dT%H:00:00Z', time.strptime(i["created_at"],'%a %b %d %H:%M:%S +0000 %Y'))
        i["tweet_date"] = tweet_date
"""
