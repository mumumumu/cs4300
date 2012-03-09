'''
Created on Oct 08, 2011

@author: jeff
'''
from urllib2 import urlopen
from re import split
from math import log10
from numpy import concatenate, dot, zeros
from scipy import linalg
import pickle

def word_scrub(text):
    cleaned_words = []
    word_list = split('\s+', text)
    for i, word in enumerate(word_list):
        wnormalized = word.lower()
        if(wnormalized != "" and wnormalized[0].isalpha()):
            cleaned_words.append((i, wnormalized))
    return cleaned_words

def inverted_index_doc(text):
    inverted = {}
    for index, word in text:
        locations = inverted.setdefault(word, [])
        locations.append(index)
    return inverted

def inverted_index_total(inverted, doc_id, doc_index):
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted    

def excerpt(docID):
    url = "http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/file%s.txt" % (docID)
    text = urlopen(url).readlines()
    for line in text:
        words = split('\s+', line)
    return words[0:10]

def search(q, Ck, numDocs):
    score = []
    s = zeros(numDocs)
    for i in range(0, numDocs):
        e = zeros(numDocs)
        e[i] = 1;
        s[i] = dot(q, dot(Ck, e)) / (linalg.norm(q) * linalg.norm(dot(Ck, e)))
    s = s / max(s)
    for i in range(0, len(s)):
        score.append((s[i], i))
    score = sorted(score, reverse=True)
    for sc, docID in score[0:5]:
        docID = "%.2d" % (docID)
        print "file%s - Normalized Score:%.4f" % (docID, sc)        
        print "\t%s\n" % (" ".join(excerpt(docID)))
        
         
inverted = {}
numDocs = 40
print "Indexing documents from http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/"
for i in range(0, numDocs):
    fileIndex = "%.2d" % (i)
    url = "http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/file%s.txt" % (fileIndex)
    text = urlopen(url)
    contents = text.readlines()
    for line in contents:
        words = word_scrub(line)
    docIndex = inverted_index_doc(words)
    inverted_index_total(inverted, fileIndex, docIndex)
#fout = open("inverted.dat", "w")
#pickle.dump(inverted, fout)
#fout.close()
#fin = open("inverted.dat", "r")
#inverted = pickle.load(fin)
stopwords = []
for key in sorted(inverted.iterkeys()):
    df = len(inverted[key])
    if df > ((2 * numDocs) / 3):
        stopwords.append(key)
validWords = [word for word in inverted if word not in stopwords]
tfidf_matrix = zeros((len(validWords), numDocs))
for i, t in enumerate(validWords):
    df = len(inverted[t])
    for j in inverted[t].iterkeys():
        tf = len(inverted[t][j])
        tfidf_matrix[i, j] = (1 + log10(tf)) * log10(numDocs / df)
U, S, Vt = linalg.svd(tfidf_matrix)
k = 5
Sk = linalg.diagsvd(concatenate((S[0:k], zeros(len(S) - k))), len(U), len(Vt))
Xk = dot(dot(U, Sk), Vt)

for i in range(40):
    print S[i]

while True:
    query = raw_input("\nEnter a query: ")
    if query == "ZZZ":
        break
    query = word_scrub(query)
    validQuery = [word for _, word in query if word in validWords]
    invalidWords = [word for _, word in query if word not in validWords]
    if(len(validQuery) > 0):
        q = zeros(len(validWords))
        for i, term in enumerate(validWords):
            for word in validQuery:
                if(word == term):
                    q[i] = 1
        search(q, Xk, numDocs)
    if len(invalidWords) > 0:
        print "The following words were either on the stoplist or not found: %s" % (", ".join(invalidWords))
    

    
    
    
    
