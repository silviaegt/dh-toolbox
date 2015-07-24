__author__ = 'silvia'
# Script to extract text content from Zotero HTML items
# Inspired by Spencer Roberts' tutorial:
# http://programminghistorian.org/lessons/counting-frequencies-from-zotero-items.html

###############################
# Import statements
###############################
from bs4 import BeautifulSoup, Comment
import re
import glob
import errno
from pyzotero import zotero
import requests
import unicodedata
from nltk.corpus import stopwords
from string import punctuation
import os
import csv
from collections import defaultdict, Counter


def htmlseg(html):
    with open(html) as f:
        i = f.read()
        soup = BeautifulSoup(i)
        comments = soup.findAll(text=lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]
        output = re.compile('<div class="Texto_Autor">(.*?)<script type="text/javascript">',
                            re.DOTALL | re.IGNORECASE).findall(str(soup))
        new_output = str(output).replace('\\n', ' ').replace('\\t', ' ')
        n = open('s_'+html, 'w')
        n.write(str(new_output))
        n.close()

def modbtwtag(html, pat):
    with open(html) as f:
        pattern = re.compile(pat, re.DOTALL | re.IGNORECASE)
        text = f.read()
        new = re.sub(pattern, lambda x: x.group().strip().replace('.', '').replace('\n', ' ').replace(' ', '_'), text)
        name ='a_'+html[2:]
        n = open(name, 'w')
        n.write(str(new))
        print('Working on ', name)
        n.close()
#pattern = '<a href="http://elem.mx/autor/datos/\d+">(.*?)</a>'

def html2text(file):
    """
    create a text file from a html
    """
    with open(file) as f:
        input = f.read()
        striptag = re.sub('<[^<]+?>', '', str(input))
        stripspace = ' '.join(str(striptag).split())
        title = 't_'+file[2:-5] + '.txt'
        n = open(title, 'w')
        n.write(str(striptag))
        n.close()

def txt2list(filename):
    """
    returns a list of words
    """
    words=[]
    [words.append(word.lower()) for word in (open(filename, encoding="utf-8")).read().split()]
    l=[]
    #punctuation+=["¿¡"]
    for word in words:
        [l.append(w) for w in re.split('[%s¿¡!?"«»]' % punctuation, word) if w != '']
    return l

def make_cooc_dict(l, window_size = 5):
    '''
    Takes as input a token list and a window size [ws] (default == 5)
    every time a word has a dif as it self & is btw the range of ws
    it is added to a default dictionary
    ws = distance in words both left and right from target word.
    '''
    d = defaultdict(Counter)
    for idx, word in enumerate(l):
        for idx2 in range(max(0, idx-window_size), min(len(l), idx+window_size+1)):
            if idx != idx2:
                d[word][l[idx2]] += 1
    return d

def csv_from_list(csvfile, listname):
    """
    create a csv file from a list
    """
    f = open(csvfile, 'w', encoding='utf-8')
    csv_writer = csv.writer(f, dialect='excel')
    for x in listname:
        csv_writer.writerow([x, ])
    f.close()


def list_from_csv(single_csv):
    """
    Convert csv files into lists
    """
    lista = []
    with open(single_csv, "r", encoding="utf-8") as fn:
        for line in fn:
            lista.append(line[:-1])
    return lista

###############################
# Reading my collection w/libZotero (DID NOT WORK)
###############################

#zlib = zotero.Zotero('group','155975','<null>','9GLmvmZ1K1qGAz9QWcdlyf6L')
#items = zlib.items(limit=5)

###############################
# Reading my collection w/pyzotero
# note: The Read API calls return the first 25 items by default
# solution: zlib.everything() 
###############################
# My own user ID / api key
zlib = zotero.Zotero('1677289','user','4g5SrCY6IUW1x6LPUfXrzVGe')
Collection: https://www.zotero.org/silviaegt/items/collectionKey/THA7JMA5
items = zlib.everything(zlib.collection_items('THA7JMA5'))

###############################
# Retrieving url-CONTENTS w/REQUESTS
# more info : http://docs.python-requests.org/en/latest/user/quickstart/
###############################
"""
itemlist = []
webpageitems = []
for item in items:
    #print(item['data']['title'])
    itemlist.append(item['data']['title'])
    if item['data']['itemType'] == 'webpage':
        webpageitems.append(item['data']['title'])
print(len(itemlist)) #152
print(len(webpageitems)) #76
"""
"""
webpageitems = []
itemlist = []
for item in items:
    itemlist.append(item['data']['title'].split('-')[-5])
    if item['data']['itemType'] == 'webpage':
        webpageitems.append(item['data']['title'].split('-')[-5])
print(len(itemlist))
print(len([i for i, j in zip(itemlist, webpageitems) if i not in j]))
"""
"""
os.chdir('asoc_html')
for item in items:
    if item['data']['itemType'] == 'webpage':
        url = item['data']['url']
        title = item['data']['title'].split('-')[-5].replace(',','').replace(' ','')
        filename = unicodedata.normalize('NFKD', title).encode('ASCII', 'ignore').decode("utf-8") + '.html'
        print('Saving local copy of ' + filename)
        response = requests.get(url)
        response.encoding = 'utf-8'
        webContent = response.text
        #print(webContent)
        f = open(filename, 'w')
        f.write(webContent)
        f.close()
"""
###############################
# Chopping interesting html segment
###############################
"""
#THIS IS THE ONE THAT WORKS
os.chdir('asoc_html')
for file in glob.glob("*.html"):
    try:
        htmlseg(file)
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
"""
"""
os.chdir('asoc_html')
for file in glob.glob("*.html"):
    try:
        html2seg(file)
        print('Working on ', file)
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
"""
###############################
# Convert authors in one word
###############################
"""
for file in glob.glob("*.html"):
    try:
        modbtwtag(file, '<a href="http://elem.mx/autor/datos/\d+">(.*?)</a>',
                  '.', '', ' ', '_')
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise

"""
"""
os.chdir('asoc_sec')
for file in glob.glob("*.html"):
    try:
        modbtwtag(file, '<a href="http://elem.mx/autor/datos/\d+">(.*?)</a>')
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
"""
###############################
# Retrieving elements btw tags from html segment
# and creating a list
###############################
#asocaut = defaultdict(list)
"""
aulist = []
os.chdir('asoc_html')
with open('SociedadCatolicaLa.html') as f:
    input = f.read()
    authors = re.compile('<a href="http://elem.mx/autor/datos/\d+">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(input)
    print(authors)
    authorslist = set([a for a in authors])
    for a in authorslist:
        print(a.lstrip())
        aclean = a.lstrip().replace('.', '').replace(' ', '_').replace('\n', '_')
        aulist.append(aclean.lower())
auset = sorted(set(aulist))
print(auset)
"""
"""
os.chdir('asoc_au')
aulist = []
for file in glob.glob("*.html"):
    with open(file) as f:
        input = f.read()
        #Find authors that are quoted in ELEM
        #print(output)
        authors = re.compile('<a_href="http://elemmx/autor/datos/\d+">(.*?)</a>', re.DOTALL | re.IGNORECASE).findall(input)
        authorslist = set([a for a in authors])
        for a in authorslist:
            aulist.append(a.lower())
        #asocaut[file[:-5]] = authorslist
#print(len(set(aulist)))
auclean = sorted(set(aulist))
"""
#csv_from_list('authors.csv', auclean)
#print(auclean)
#print(len(auclean))
###############################
# Find authors in text
###############################
"""
with open('AteneoMexicanoEl.txt') as f:
    text = f.read()
    authors = list_from_csv('authors.csv')
    for a, l in zip(authors, text.split('.')):
        if a in l:
            print(l)

"""

#words = re.findall('\w+', clean_text)

###############################
# From html-segment to txt
##############################
"""
os.chdir('asoc_au')
for file in glob.glob("*.html"):
    try:
        html2text(file)
    except IOError as exc:
        if exc.errno != errno.EISDIR:
            raise
"""
