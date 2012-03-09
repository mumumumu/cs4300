'''
Created on Sep 15, 2011

@author: jeff
'''
from urllib2 import urlopen
from re import split
from math import log10

def word_scrub(text):
    cleaned_words = []
    word_list = split('\s+',text)
    for i, word in enumerate(word_list):
        wnormalized = word.lower()
        if(wnormalized != "" and wnormalized[0].isalpha()):
            cleaned_words.append((i,wnormalized))
    return cleaned_words

def inverted_index_doc(text):
    inverted = {}
    for index, word in text:
        locations = inverted.setdefault(word, [])
        locations.append(index)
    return inverted

def inverted_index_total(inverted,doc_id,doc_index):
    for word, locations in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = locations
    return inverted    

def excerpt(docID,index):
    url = "http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/file%s.txt" %(docID)
    text = urlopen(url).readlines()
    for line in text:
        words = split('\s+',line)
    if index-5>0:
        return words[index-5:index+5]
    else:
        return words[index-index:index+10]
    
def search(query,inverted,numDocs,stoplist):
    if len(query)==1:
        for _,word in query:
            if word in inverted:
                df = len(inverted[word])
                for doc in sorted(inverted[word].iterkeys()):
                    tf = len(inverted[word][doc])
                    tfidf = (1+log10(tf))*log10(numDocs/df)
                    print "\ttf=%d, df=%d, tf*idf=%.2f"%(tf,df,tfidf)
                    print "\tfile%s: %s"%(doc,inverted[word][doc])
                    context = excerpt(doc,inverted[word][doc][0]);
                    print "\t%s\n"%(" ".join(context))
            else:
                print "Your search - %s - did not match any documents."%(word)
    else:
        validWords = [word for _, word in query if word in inverted and word not in stoplist]
        invalidWords = [word for _,word in query if word not in validWords]
        matches = [set(inverted[k].keys()) for k in validWords]
        matches = list(reduce(lambda x, y: x & y, matches) if matches else [])
        results = []
        for doc in matches:
            tfidf=0
            for word in validWords:
                df = len(inverted[word])
                tf = len(inverted[word][doc])
                tfidf = tfidf+(1+log10(tf))*log10(numDocs/df)
            results.append((tfidf,doc))
        for tfidf,doc in sorted(results,None,None,True):
            print "\tfile%s: tfidf=%.3f"%(doc,tfidf)
        if len(invalidWords)>0:
            print "The following words were either on the stoplist or not found: %s"%(", ".join(invalidWords))
         
inverted={}
numDocs=40
print "Indexing documents from http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/"
for i in range(0,numDocs):
    fileIndex = "%.2d"%(i)
    url = "http://www.infosci.cornell.edu/Courses/info4300/2011fa/test/file%s.txt" %(fileIndex)
    text = urlopen(url)
    contents = text.readlines()
    for line in contents:
        words = word_scrub(line)
    docIndex = inverted_index_doc(words)
    inverted_index_total(inverted,fileIndex,docIndex)
    
index = 1
stopwords=[]
#file1 = open('3.txt','w')
#file1.write('%s,%s\n'%('Word','df'))
for key in sorted(inverted.iterkeys()):
    df = len(inverted[key])
    #file1.write('%s,%d\n'%(key,df))
    print "%d %s [%d]"%(index,key,df)
    for doc in sorted(inverted[key].iterkeys()):
        tf = len(inverted[key][doc])
        print "\tfile%s [%d]: %s"%(doc,tf,inverted[key][doc])
    index = index+1
    if df>((2*numDocs)/3):
        stopwords.append(key)
while True:
    query = raw_input("\nEnter a query: ")
    if query == "ZZZ":
        break
    query = word_scrub(query)
    result = search(query,inverted,numDocs,stopwords)


    
    
    
    