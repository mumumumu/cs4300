'''
Created on Nov 1, 2011

@author: jeff
'''
from urllib2 import urlopen
import re
from bs4 import BeautifulSoup
from numpy import dot, zeros, set_printoptions, ones
import pickle

def normalize_url(url):
    if url.endswith('/index'):
        return url[0:len(url) - 6]
    elif url.endswith('/index.html'):
        return url[0:len(url) - 11]
    elif url.endswith('/'):
        return url[0:len(url) - 1]
    else:
        return url

def find_outlinks(i):
    current_directory = i   
    html = urlopen(i).read()
    url_list = []
    soup = BeautifulSoup(html)
    anchors = soup.find_all('a')
    title = soup.find('title').string
    title_list.append(title)
    for a in anchors:
        if a.has_attr('href'):
            out_link = str(a['href'])
            # normalize links
            if not out_link.startswith('www') and not out_link.startswith('http'): 
                if out_link.startswith('/'):
                    out_link = host + out_link[1:]
                elif out_link.startswith('../'):
                    for i in xrange(out_link.count('../')):
                        out_link = out_link[3:]
                        t_directory = current_directory[0:current_directory.rfind('/')]
                    out_link = t_directory + '/' + out_link 
                else:
                    out_link = current_directory + out_link
            if a.img != None:
                if a.img.has_attr('alt'):
                    anchor_text = str(a.img['alt'])
                else:
                    anchor_text = str(a.img['src'])
            else:
                anchor_text = str(a.string)
            if anchor_text != ' ' and anchor_text != 'None':
                out_link = normalize_url(out_link)
                if out_link in test_set:
                    url_list.append((out_link, anchor_text)) #remove index at end bc some may be /index
    return url_list

def write_files():
    fout = open("metadata.txt", "w")
    for k, i in enumerate(metadata):
        string = str(i[0]) + '. ' + test_set[k] + '\n\tPageRank = ' + str(i[1]) + '\n\tTitle = ' + str(i[2]) + '\n\tAnchor Text = ' + str(i[3]) + '\n'
        fout.write(string)
    fout.close()
    fout = open("short_index_record.txt", "w")
    pickle.dump(short_index_record, fout)
    fout.close()
    fout = open("pagerank.txt", "w")
    pickle.dump(pageRank, fout)
    fout.close()
    fout = open("metadata.dat", "w")
    pickle.dump(metadata, fout)
    fout.close()

def build_link_matrix():
    set_printoptions(threshold='nan')
    #normalize all urls in test set before start extracting
    for k, i in enumerate(test_set):
        test_set[k] = normalize_url(i)
    for k, i in enumerate(test_set):
        if not i.endswith('css'): 
            outlinks = find_outlinks(i)
            #print i
            #print outlinks
        else:
            title_list.append('css')
            outlinks = []
        if len(outlinks) == 0:
            dead_end.append(k)    
        else:
            for link in outlinks:
                link_matrix[k, test_set.index(link[0])] = 1
                inlink_anchors.setdefault(test_set.index(link[0]), []).append((k, link[1]))

def calc_pagerank():
    alpha = .15
    # create transition matrix 
    transition_matrix = zeros((nPages, nPages))
    for i in xrange(nPages):
        if i in dead_end:
            transition_matrix[i, :] = float(1.0 / nPages)
        else:
            transition_matrix[i, :] = (1 - alpha) * (link_matrix[i, :] / link_matrix[i, :].sum()) + alpha / nPages
    # calculate page rank
    pageRank = ones((1, nPages)) / nPages
    for i in xrange(100):
        pageRank = dot(pageRank, transition_matrix)  

def build_record():
    # short index record
    short_index_record = []
    for key, val in inlink_anchors.iteritems():
        short_index_record.append((str(title_list[key]), list(set([a[1] for a in val]))))
    for i in xrange(nPages):
        title = str(title_list[i])
        anchor = []
        if i in inlink_anchors and not (inlink_anchors[i] is None):
            anchor = list(set([a[1] for a in inlink_anchors[i]]))
        short_index_record.append((title, anchor))
    # metadata
    for k, i in enumerate(short_index_record):
        metadata.append((k, pageRank[0][k], short_index_record[k][0], short_index_record[k][1]))
     
def search(term):
    results = []
    term = term.lower()
    for k, _ in enumerate(metadata):
        data = metadata[k][2] + ' ' + (' ').join(metadata[k][3])
        if term in data.lower():
            results.append((metadata[k][1], metadata[k][0], test_set[k], metadata[k][2], metadata[k][3])) 
    results = sorted(results, reverse=True)
    return results[0:10]
   
# MAIN
url = "http://www.infosci.cornell.edu/courses/info4300/2011fa/test/test3.txt"
test_set = re.split('\n', urlopen(url).read())
test_set.pop();     #removes the last element which is just ''
host = "http://www.library.cornell.edu/"

#initiate objects
title_list = []
nPages = len(test_set)
link_matrix = zeros((nPages, nPages))
dead_end = []
inlink_anchors = {}
metadata = []
pageRank = []
short_index_record = []

# open files
'''fin = open("short_index_record.txt", "r")
short_index_record = pickle.load(fin)
fin2 = open("pagerank.txt", "r")
pageRank = pickle.load(fin2)'''
fin3 = open("metadata.dat", "r")
metadata = pickle.load(fin3)

while True:
    query = raw_input("\nEnter a single term query: ")
    if query == "ZZZ":
            break
    results = search(query)
    if len(results) != 0:
        for i, r in enumerate(results):
            print str(i + 1) + '. (' + str(r[1]) + ') ' + str(r[2]) 
            print '\tPageRank = ' + str(r[0])
            print '\tTitle: ' + r[3]
            print '\tAnchor Text: ' + str(r[4]) 
    else:
        print "No results found for - " + query       

