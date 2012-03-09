'''
Created on Dec 4, 2011

@author: jeff
'''
import pickle
import math
def mutual_info(w, c):
    n11 = 0
    n00 = 0
    n10 = 0
    n01 = 0
    for d in c:
        if d[1].has_key(w):
            n11 += 1.0
        else:
            n00 += 1.0
    for b in clusters:
        if b != c:
            for d in b:
                if d[1].has_key(w):
                    n10 += 1.0
                else:
                    n01 += 1.0
    n = n11 + n00 + n01 + n10
    n1_ = n10 + n11
    n_1 = n01 + n11
    n0_ = n00 + n01
    n_0 = n00 + n10
    a1 = n11 / n
    b1 = n10 / n
    c1 = n01 / n
    d1 = n00 / n
    if n11 == 0 or n1_ == 0 or n_1 == 0:
        a2 = 0
    else:
        a2 = math.log((n * n11) / (n1_ * n_1), 2)
    if n10 == 0 or n1_ == 0 or n_0 == 0:
        b2 = 0
    else:
        b2 = math.log((n * n10) / (n1_ * n_0), 2)
    if n01 == 0 or n0_ == 0 or n_1 == 0:
        c2 = 0
    else:
        c2 = math.log((n * n01) / (n0_ * n_1), 2)    
    if n00 == 0 or n0_ == 0 or n_0 == 0:
        d2 = 0
    else:
        d2 = math.log((n * n00) / (n0_ * n_0), 2)
    
    minfo = (a1 * a2 + b1 * b2 + c1 * c2 + d1 * d2)
    return minfo
  

fin = open("clusters.dat", "r")
clusters = pickle.load(fin)
fin.close()

fin = open("valid_words.dat", "r")
word_index = pickle.load(fin)
fin.close()

minfo = []
docs = []
match = {}
n = 0

for c in clusters:
    minfo.append([])
    for w in word_index:
        minfo[n].append((mutual_info(w, c), w))
    n += 1
n = 0
for c in minfo:
    c.sort(reverse=True)
    print n
    for i in xrange(10):
        print c[i]
    print '\n'
    n += 1

top10 = [64, 66, 67, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87]
n = 0
for c in clusters:
    for d in c:
        if d[0] in top10:
            match.setdefault(n, [])
            match[n].append(d[0])
    n += 1
    
#for m in match:
#   print m, set(match[m])
    
