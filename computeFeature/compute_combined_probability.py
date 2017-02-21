#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file compute_third_map.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire token for its probability of reopen 
# **
"""

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from combine_description_comments import hasNumbers


def extract_description(filename, desc_file):
    output = open(desc_file, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 16:
                bug_id = mid[0]
                desc = mid[13].replace('[u', ' ')
                desc = desc.replace('[', ' ')
                desc = desc.replace(']', ' ')
                desc = desc.replace('\\n', ' ')
                desc = desc.replace('u"', ' ')
                desc = desc.replace("u'", ' ')
                description = re.sub(r"\s{2,}", " ", desc)
                output.write(bug_id)
                output.write('\t')
                output.write(description)
                output.write('\n')
    output.close()


def extract_comments(filename, comms_file):
    output = open(comms_file, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 16:
                bug_id = mid[0]
                comm = mid[14].replace('[u', ' ')
                comm = comm.replace('[', ' ')
                comm = comm.replace(']', ' ')
                comm = comm.replace('\\n', ' ')
                comm = comm.replace('u"', ' ')
                comm = comm.replace("u'", ' ')
                comments = re.sub(r"\s{2,}", " ", comm)
                output.write(bug_id)
                output.write('\t')
                output.write(comments)
                output.write('\n')
    output.close()

def compute_combined_prob(filename, third_dictfile, outfile):
    third_dict = {}
    output = open(outfile, 'w')
    with open(third_dictfile) as f:
        for line in f:
            line = line.strip()
            mid = line.split(':')
            #if len(mid) == 2:
            third_dict[mid[0]] = mid[1]
    with open(filename) as of:
        for line in of:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 1:
                output.write(mid[0])
                output.write('\t')
                output.write(str(0.5))
                output.write('\n')
            if len(mid) == 2:
                print mid[0]
                probs = compute_fifteen_token(third_dict, mid[1])
                prod = 1
                for prob in probs:
                    prod = prod * float(prob)
                for i in range(len(probs)):
                    probs[i] = 1 - float(probs[i])
                a = 1
                for prob in probs:
                    a = a * float(prob)
                b = prod + a
                score = prod / b
                output.write(mid[0])
                output.write('\t')
                output.write(str(score))
                output.write('\n')
    output.close()

def compute_fifteen_token(third_dict, text):
    text = text.strip()
    words = text.split(' ')
    token_prob = {}
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
                if token not in third_dict:
                    token_prob[token] = 0.4
                else:
                    token_prob[token] = third_dict[token]
    dict_for_sort = {}
    for key in token_prob:
        dict_for_sort[key] = abs(float(token_prob[key]) - 0.5)
    sorted_token_probs = sorted(dict_for_sort.items(), key = lambda item:item[1], reverse=True)
    probs = []
    i = 0
    while i < 15 and i < len(token_prob):
        print sorted_token_probs[i][0]
        print token_prob[sorted_token_probs[i][0]]
        probs.append(token_prob[sorted_token_probs[i][0]])
        i = i + 1
    return probs


def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/bugReport/Mozilla_reopen_1.txt"
    desc_file = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/reopen_description.txt"
    comms_file = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/reopen_comments.txt"
    third_dictfile = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/third_dict.txt"
    desc_scorefile = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/reopen_desc_score.txt"
    comms_scorefile = "/home/carrie/scrapyCrawe/computeFeature/Mozilla/reopen_comms_score.txt"
    extract_description(filename, desc_file)
    extract_comments(filename, comms_file)
    compute_combined_prob(desc_file, third_dictfile, desc_scorefile)
    compute_combined_prob(comms_file, third_dictfile, comms_scorefile)

if __name__ == "__main__":
    main()
