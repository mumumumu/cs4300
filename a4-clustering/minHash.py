'''
Created on Dec 3, 2011

@author: jeff
'''
import os
import re
import random
import pickle

def words(text):
    return re.split('\s+', text.lower())

def get_shingles(text, size):
    word_list = [w for w in words(text) if w != ''] 
    shingle_list = [word_list[i:i + size] for i in range(len(word_list) - size + 1)]
    [shingle_index.append(i) for i in shingle_list if not shingle_index.count(i)]
    return [i for i, v in enumerate(shingle_index) if v in shingle_list]

def transform_doc_shingles():
    for s in doc_shingles:
        doc_shingles_transform.append(sketch_doc(s))

def sketch_doc(s):
    sketch = []
    for a_s, b_s in zip(a, b):
        q = [((a_s * x + b_s) % p) for x in s]
        q.sort()
        sketch.append(q[0])
    return sketch

def jaccard_estimate(doc1, doc2):     
    n = 0
    for x, y in zip(doc1, doc2):
        if x == y:
            n += 1
    return float(n) / float(n_functions)

def jaccard_actual(doc1, doc2):
    d1 = set(doc1)
    d2 = set(doc2)
    x = len(d1.intersection(d2))
    y = len(d1.union(d2))
    return float(x) / float(y)

def jaccard():
    for i, d1 in enumerate(doc_shingles_transform):
        jc = []
        for j, d2 in enumerate(doc_shingles_transform):
            if i < j and jaccard_estimate(d1, d2) > .5:
                duplicates.append((i, j, jaccard_actual(doc_shingles[i], doc_shingles[j])))
            if i < 10 and i != j:
                jc.append((jaccard_estimate(d1, d2), i, j))
        if i < 10:
            jc.sort(reverse=True)
            top10.append(jc[0:3])       

def save_shingle_index():
    fout = open("shingle_index.txt", "w")
    for i, v in enumerate(shingle_index):
        fout.write(str(i) + " " + str(v) + "\n")    
    fout.close()
    fout = open("shingle_index2.dat", "w")
    pickle.dump(shingle_index, fout)
    fout.close()
    fout = open("doc_shingles.txt", "w")
    for i, v in enumerate(doc_shingles):
        fout.write(str(i) + " " + str(v) + "\n")    
    fout.close()
    fout = open("doc_shingles2.dat", "w")
    pickle.dump(doc_shingles, fout)
    fout.close()
        
def print_doc_shingles():
    for i, v in enumerate(doc_shingles):
        print str(i) + " " + str(v)
    for i, v in enumerate(doc_shingles):
        print str(i) + " " + str(v)

def read_files(directory):
    for infile in os.listdir(directory):
        print "current file is: " + infile
        f = open(directory + '/' + infile).read();
        doc_shingles.append(get_shingles(f, shingle_size))

shingle_index = []
doc_shingles = []
doc_shingles_transform = []
duplicates = []
top10 = []
shingle_size = 3
n_functions = 25
p = 23789
a = [random.randint(1, p - 1) for x in xrange(n_functions)]
b = [random.randint(0, p - 1) for x in xrange(n_functions)]
#read_files('test')

fin = open("shingle_index.dat", "r")
shingle_index = pickle.load(fin)
fin = open("doc_shingles.dat", "r")
doc_shingles = pickle.load(fin)
save_shingle_index()
transform_doc_shingles()
jaccard();

print "The following documents have Jaccard coefficient greater than .5:"
for i in duplicates:
    print "J(%d,%d) = %f" % (i[0], i[1], i[2])
match = []
match_dict = {}

print "\n"
for i in top10:
    print "Jaccard estimates for the nearest neighbors to file0%d.txt" % (i[0][1])
    for j in i:
        match_dict.setdefault(j[1], [])
        match_dict[j[1]].append(j[2])
        match.append(j[2])
        print "J(%d,%d) = %f" % (j[1], j[2], j[0])
    print ''
#print set(match)
#print match_dict
