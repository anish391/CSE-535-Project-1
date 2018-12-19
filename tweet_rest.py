#!/usr/bin/env python
# encoding: utf-8

import tweepy
import json
import time

#Twitter API credentials
consumer_key = "HBy7StkBrv0w67zlqRnnhvsPO"
consumer_secret = "WFt5drHQMMfPFv09TgejJkKpciZwH5wMNNQptKvZY2FQsaSZ41"
access_key = "105377073-QCwpfWm8L5NOBVq8XpWB6N1FvfeahQtGE37QHKjz"
access_secret = "uMdsgCkAZyxgkySr8mXukeGpVT1e0aDXC4lg3Kdy9pbVp"


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
#refer http://docs.tweepy.org/en/v3.2.0/api.html#API
#tells tweepy.API to automatically wait for rate limits to replenish

#Put your search term
searchquery_environment = '"air quality" OR floods OR nature OR wildlife OR drought OR hurricane OR "global warming" OR toxic OR pollution OR ozone OR "climate change" OR "clean energy" OR sustainable OR sustainability -RT'
searchquery_crime = 'armed OR robbery OR cartels OR gun OR hostage OR stone OR kill OR killed OR 911 OR hostage OR killings OR DUI OR murder OR victim OR dead OR assault OR police OR terrorist OR bombing OR assault OR gun OR knife OR #justice OR drugs -RT'
searchquery_politics = 'politics OR rajneeti OR BJP OR Kejriwal OR #1stAmmendment OR #FreedomOfThePress OR federal OR @realDonaldTrump OR @narendramodi OR #CountryOverParty OR "Donald Trump" OR Trump OR Hillary OR Clinton OR election OR senate OR #BringitHome OR budget OR "Narendra Modi" OR democracy OR democrat OR republican OR "Justin Trudeau" OR "White House" OR congress OR parliament -RT'
searchquery_social_unrest = '"tear gas" OR "civil disorder" OR propaganda OR "political assassination" OR "Andrei Karlov" OR "revolt" OR "protest" OR "violent protest" OR riot OR riots OR "stone throwing" OR "stones thrown" -RT'
searchquery_infra = '#infrastucture OR infrastructure OR construction dam OR construction road OR "under construction" OR slab OR concrete OR contractors OR groundwork OR building OR bridge OR "work site" OR "construction site" -website -RT'


#mexico = "19.4326,-99.1332,40mi"
#delhi = "28.7041, 77.1025"
#bangkok = "13.7563,100.5018,40mi"
#nyc = "40.7128,-74.0060,40mi"
#paris = "48.8566,2.3522,40mi"
users =tweepy.Cursor(api.search,q=searchquery_infra, geocode='28.7041, 77.1025,100mi', lang='en').items()
count = 0
errorCount=0
file = open('infra_hi_delhi_21nov.json', 'w') # CHANGE DIS
while True:
    try:
        user = next(users)
        #use count-break during dev to avoid twitter restrictions
        #if (count>10):
        #    break
    except tweepy.TweepError:
        #catches TweepError when rate limiting occurs, sleeps, then restarts.
        #nominally 15 minnutes, make a bit longer to avoid attention.
        print("sleeping....")
        time.sleep(60*16)
        user = next(users)
    except StopIteration:
        break
    try:
        count += 1
        #if(count==3901):
        #    break
        print("Writing to JSON tweet number:"+str(count))
        user._json["topic"]="infra"# CHANGE DIS
        user._json["city"]="delhi"# CHANGE DIS
        user._json["tweet_loc"] = "28.7041, 77.1025" #CHANGE DIS
        json.dump(user._json,file,sort_keys = True,indent = 4)
        
    except UnicodeEncodeError:
        errorCount += 1
        print("UnicodeEncodeError,errorCount ="+str(errorCount))

print("completed, errorCount ="+str(errorCount)+" total tweets="+str(count))
    
    #todo: write users to file, search users for interests, locations etc.

"""
http://docs.tweepy.org/en/v3.5.0/api.html?highlight=tweeperror#TweepError
NB: RateLimitError inherits TweepError.
http://docs.tweepy.org/en/v3.2.0/api.html#API  wait_on_rate_limit & wait_on_rate_limit_notify
NB: possibly makes the sleep redundant but leave until verified.

"""

