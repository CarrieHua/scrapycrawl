#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file combine_description_comments.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire the combination of description and comments which will act corpus for computing the times of each token in the corpus
# **
"""

import os
import string
import random
from sets import Set
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def combine_description_comments(filename, outfile):
    """
    input: filename, the file which store the crawled data; 
    outfile: the file contain description and comments
    example:bug_id  description comments
    """
    output = open(outfile, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split("\t")
            if len(mid) == 16:
                bug_id = mid[0]
                desc = mid[13].replace('[u', ' ')
                desc = desc.replace('[', ' ')
                desc = desc.replace(']', ' ')
                desc = desc.replace('\\n', ' ')
                desc = desc.replace('u"', ' ')
                desc = desc.replace("u'", ' ')
                description = re.sub(r"\s{2,}", " ", desc)
                comm = mid[14].replace('[u', ' ')
                comm = comm.replace('[', ' ')
                comm = comm.replace(']', ' ')
                comm = comm.replace('\\n', ' ')
                comm = comm.replace('u"', ' ')
                comm = comm.replace("u'", ' ')
                comments = re.sub(r"\s{2,}", " ", comm)
                output.write(bug_id)
                output.write('\t')
                output.write(description)
                output.write(' ')
                output.write(comments)
                output.write('\n')
    output.close()


def copyfile(srcfile, dstfile, linenum):
    """
    get linenum different lines out from srcfile at random and write them into dstfile
    srcfile:bug_id  description comments
    dsffile:bug_id  description comments
    """
    result = []
    ret = False
    try:
        srcfd = open(srcfile, 'r')
    except IOError:
        print 'srcfile doesnot exist!'
        return ret
    try:
        dstfd = open(dstfile, 'w')
    except IOError:
        print 'dstfile doesnot exist!'
        return ret
    srclines = srcfd.readlines()
    srclen = len(srclines)
    while len(Set(result)) < int(linenum):
        s = random.randint(0, srclen - 1)
        result.append(srclines[s])
    for content in Set(result):
        dstfd.write(content)
    srcfd.close()
    dstfd.close()
    ret = True
    return ret


def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

def compute_token_times(filename, outfile):
    output = open(outfile, 'w')
    token_times = {}
    with open(filename) as of:
        for line in of:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 2:
                content = mid[1].strip()
                words = content.split(' ')
                for word in words:
                    word = word.strip()
                    if word == "" or hasNumbers(word):
                        continue
                    word = re.sub('[^a-zA-Z]',' ', word)
                    tokens = word.split(' ')
                    for token in tokens:
                        token = token.strip()
                        if token:
                            token = token.lower()
                            if token not in token_times:
                                token_times[token] = 0
                            token_times[token] = token_times[token] + 1
    for key in token_times:
        output.write(key)
        output.write(':')
        output.write(str(token_times[key]))
        output.write('\n')
    return token_times


def main():
    """
    main function
    """
    linenum = 4000
    filename = "/home/carrie/scrapyCrawe/bugReport/Mozilla_nonReopen_1.txt"
    srcfile = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/nonReopen_description_comments.txt"
    dstfile = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/corpus_nonReopen.txt"
    maps_file = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/nonReopen_token_times.txt"
    combine_description_comments(filename, srcfile)
    copyfile(srcfile, dstfile, linenum)
    compute_token_times(dstfile, maps_file)


if __name__ == "__main__":
    main()
