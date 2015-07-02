__author__ = 'silvia'
# Script to extract text content from Zotero HTML items
# Inspired by Spencer Roberts' tutorial: http://programminghistorian.org/lessons/counting-frequencies-from-zotero-items.html 


###############################
# Import statements
###############################

#from bs4 import BeautifulSoup
#from libZotero import zotero
#import urllib.request
import re
from pyzotero import zotero
import requests
from nltk.corpus import stopwords



#zlib = zotero.Zotero('group','155975','<null>','9GLmvmZ1K1qGAz9QWcdlyf6L')
#items = zlib.items(limit=5)

###############################
# Reading my collection w/pyzotero
###############################
zlib = zotero.Zotero('1677289','user','4g5SrCY6IUW1x6LPUfXrzVGe') # My own user ID / api key
items = zlib.collection_items('THA7JMA5') # My collection: https://www.zotero.org/silviaegt/items/collectionKey/THA7JMA5

###############################
# Retrieving url-content w/REQUESTS
# more info : http://docs.python-requests.org/en/latest/user/quickstart/
###############################

"""for item in items:
    print(item['data']['title'])
    #if item['data']['itemType'] == 'webpage':
        #print(item['data']['url'], ['data']['url'])
"""

for item in items:
    if item['data']['itemType'] == 'webpage':
        url = item['data']['url']
        filename = url.split('/')[-1] + '.html'
        print('Saving local copy of ' + filename)
        response = requests.get(url)
        response.encoding = 'utf-8'
        webContent = response.text
        #print(webContent)
        f = open(filename,'w')
        f.write(webContent)
        f.close()

#PROBLEM! ONLY RETRIEVING THE FIRST 25 ITEMS OF MY COLLECTION

###############################
# Retrieving url-content with URLLIB
###############################
# SYNTAX:
#response = urllib.request.urlopen(url)
#webContent = response.read()
#f.write(webContent.decode('utf-8'))
# PROBLEMS:
# urllib socket.timeout: timed out


###############################
# Get text from Website w/BeautifulSoap
# [not that great for me]
###############################

#html_doc = urllib.request.urlopen('http://www.elem.mx/estgrp/datos/104').read()
#soup = BeautifulSoup(html_doc, 'html.parser')
#text = soup.get_text()
#print(text)



###############################
# Clean text from Spanish-stopwords w/nltk
###############################

"""
def stripNonAlphaNum(text):
    return re.compile(r'\W+', re.UNICODE).split(text.lower())

def removeStopwords(wordlist):
    words = re.findall(r'\w+', str(wordlist))
    return [w for w in words if w not in stopwords.words('spanish')]

#sentence = 'El problema del matrimonio es que se acaba todas las noches despues de hacer el amor, y hay que volver a reconstruirlo todas las mañanas antes del desayuno.'
"""