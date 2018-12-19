#!/usr/bin/env python
# encoding: utf-8
import time
import json
from glob import glob
import re
from string import punctuation
import copy
from datetime import datetime
#from nltk.corpus import stopwords

# u'\U0001F300-\U0001F64F'
#                                     u'\U0001F680-\U0001F6FF'
special_symbols_pattern = re.compile(u'['u'\U0001F680-\U0001F6FF'
                                    u'\U0001F600-\U0001F64F'
                                    u'\U0001F300-\U0001F5FF'
                                    u'\U0001F1E0-\U0001F1FF'
                                    ']+', 
                                    re.UNICODE)

#list of all punctuations
punctuations = list(punctuation)

#list of langs allowed
langs = ['en','es','fr','hi','th']

#stop words dict for each language
stop_words = {'en':open("misc\sw_english.txt",encoding='utf-8').read().split("\n"),
 				"es":open("misc\sw_spanish.txt",encoding='utf-8').read().split("\n"), 
                "th":open("misc\sw_thai.txt",encoding='utf-8').read().split("\n"),
                "hi":open("misc\sw_hindi.txt",encoding='utf-8').read().split("\n"),
                "fr":open("misc\sw_french.txt",encoding='utf-8').read().split("\n")}

#list of kaomojis
kaomojis = open("misc/kaomojis.txt",encoding='utf-8').read().split("\n")

count = 0
for x in glob("*.json"):
    with open(x, "r+",encoding='utf-8') as f:
        count=0
        print("Preprocessing File :",x)
        starttime = time.time()
        data = json.load(f)
        for tweets in data:
            if tweets['lang'] in langs:
                #tweet = {}
                text = tweets['text']
                #print(tweets["id"])
                #print("preprocessed",count,"tweets.")
                #count+=1

            # Separate fields that index : hashtags, mentions, URLs, emoticons+ (emoticons + emojis
            # + kaomojis)
                tweets['hashtags'] = [k['text'] for k in tweets['entities']['hashtags']]
                for hashtag in tweets['hashtags']:
                    text = text.replace("#"+hashtag,' ')

                tweets['mentions'] = [k['screen_name'] for k in tweets['entities']['user_mentions']]
                for user_mentions in tweets['mentions']:
                    text = text.replace("@"+user_mentions,' ')

                url_list = [k['url'] for k in tweets['entities']['urls']]
                if 'media' in tweets:
                    url_list.extend([k['url'] for k in tweets['media']['url']])
                    tweets['tweet_urls'] = url_list 
                    for url in tweets['tweet_urls']:
                        text = text.replace(url, ' ')


                emojis = []
                emojis.extend(special_symbols_pattern.findall(text))
                text = re.sub(special_symbols_pattern,' ',text)
                for emo in kaomojis:
                    emojis.extend(re.findall(re.escape(emo),text))
                    text = re.sub(re.escape(emo),' ',text)
                    #print(emojis)
                    tweets['tweet_emoticons'] = emojis

                    #removing punctutations + quotes sybmbole
                for punct in punctuations+[u'\u201c',u'\u201d']:
                    text = text.replace(punct, ' ')

                #removing stopwords
                # text = text.encode("utf8")
                for stopword in stop_words[tweets['lang']]:
                    text = re.sub(re.escape(" " + stopword + " "), " ",text)

                #removing extra whitespaces
                text = ' '.join(text.split())

                # One copy of the tweet text that retains all content (see below) irrespective of the
                # language. This field should be set as the default field while searching.
                tweets['tweet_text'] = tweets['text']

                # Additionally index date, geolocation (if present), and any other fields you may like.
                #tweet['id'] = tweets['id']

                tweets['tweet_lang'] = tweets['lang']

                try:
                    tweets['tweet_date'] = datetime.fromtimestamp(int(tweets['timestamp_ms'])/1000).strftime("%Y-%m-%dT%H:00:00Z")
                except KeyError:
                    tweets['tweet_date'] = datetime.strptime(re.sub(r"\+[0-9]{4} ","",tweets['created_at']),"%a %b %d %H:%M:%S %Y").strftime("%Y-%m-%dT%H:00:00Z")

                for lang in langs:
                    if lang == tweets['lang']:
                        tweets['text_'+lang] = text

    with open(x, 'w') as outfile: 
        json.dump(data, outfile, sort_keys=True, indent=4)
    print("time taken = %s"%(time.time()-starttime))
