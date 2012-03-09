'''
Created on Dec 3, 2011

@author: jeff
'''
import math
import random
import os
import re
import pickle 

def calc_centroid(cluster):        
    centroid = {}
    for doc in cluster:
        for term in doc:
            centroid.setdefault(term, 0)
            centroid[term] += doc[term]
    return dict((term, float(centroid[term]) / float(len(cluster))) for term in centroid)

def norm(doc):
    norm = math.sqrt(sum([doc[i]*doc[i] for i in doc]))
    return dict((i, doc[i] / norm) for i in doc)

def cos(doc1, doc2):
    dot = 0
    d1 = norm(doc1)
    d2 = norm(doc2)
    for i in doc1:
        if doc2.has_key(i):
            dot += d1[i]*d2[i]
    return dot

def dist_sqd(doc1, doc2):
    #d1 = norm(doc1)
    #d2 = norm(doc2)
    return 2 * (1 - cos(doc1, doc2))

def calc_rss(cluster):
    rss = 0
    centroid = calc_centroid(cluster)
    for x in cluster:
        rss += dist_sqd(x, centroid)
    return rss

def kmeans(docs, k):
    centroids = random.sample(docs, k)
    p = 10
    #
    for _ in xrange(p):
        #initialize the clusters
        save_clusters = [[] for _ in xrange(k)] 
        clusters = [[] for _ in xrange(k)] 
        #find closest centroid for each document                
        for j in xrange(len(docs)):
            closest_centroid = 0
            for m in xrange(k):
                if dist_sqd(centroids[m], docs[j]) < dist_sqd(centroids[closest_centroid], docs[j]):
                    closest_centroid = m
            clusters[closest_centroid].append(docs[j])
            save_clusters[closest_centroid].append((j, docs[j]))
        #recompute the centroids  
        centroids = [calc_centroid(clusters[i]) for i in xrange(k)]     
        rss = 0
        for i in xrange(k):
            rss += calc_rss(clusters[i])
    #
    print "RSS = %f" % (rss)
    #rss1 = rss
    return save_clusters

def index_docs(directory):
    num_docs = 0 
    for infile in os.listdir(directory):
        text = open(directory + '/' + infile).read();
        word_list = [w for w in re.findall('[a-z]+', text.lower())  if w != ''] 
        doc = {}
        for word in word_list:
            word_index.setdefault(word, [])
            word_index[word].append(num_docs)
            doc.setdefault(word, 0)
            doc[word] += 1
        for word in doc:
            doc[word] = 1 + math.log10(doc[word])
        doc_index[num_docs] = doc
        num_docs += 1      
    for word in word_index:
        df = len(list(set(word_index[word])))
        if df > ((3 * num_docs) / 5):
            stopwords.append(word)
    for doc in doc_index:
        doc_vectors.append({})
        for word in doc_index[doc]:
            if word not in stopwords:
                #index = [i for i, w in enumerate(word_index) if w == word]
                doc_vectors[doc].setdefault(word, 0)
                doc_vectors[doc][word] = doc_index[doc][word]

doc_index = {}
stopwords = []
doc_vectors = []
word_index = {}
docs = []
valid_words = []
index_docs('test')
save_clusters = []

'''for word in word_index:
    if word not in stopwords:
        valid_words.append(word)
    else:
        print word
fout = open("valid_words.dat", "w")
pickle.dump(valid_words, fout)
fout.close()'''

k = 7
#rss1 = 100
#while rss1 > 85:
#    save_clusters = kmeans(doc_vectors, 7)
#print 'done'
print "calculating kmeans with k = %d" % (k)
save_clusters = kmeans(doc_vectors, k)
#n = 0
#for c in save_clusters:
#    print "cluster %d" % (n)
#    print c
#    n += 1
fout1 = open("clusters.dat", "wb")
pickle.dump(save_clusters, fout1)
fout1.close()

#for n in range(2, 16):
    #print n
    #kmeans(doc_vectors, n)
