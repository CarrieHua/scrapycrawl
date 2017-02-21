#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file compute_description_size.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire description size 
# **
"""

import os
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def extract_description(filename, outfile):
    """
    input: filename, the file which store the crawled data; 
    outfile: the file contain description
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
                output.write(bug_id)
                output.write('\t')
                output.write(description)
                output.write('\n')
    output.close()

def compute_description_size(filename, outfile):
    output = open(outfile, 'w')
    pattern = re.compile('[a-zA-Z]{1,}')
    with open(filename) as of:
        for line in of:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 1:
                output.write(line)
                output.write('\t')
                output.write(' ')
                output.write('\t')
                output.write(str(0))
                output.write('\n')
            if len(mid) == 2:
                desc = mid[1].split(' ')
                count = 0
                for word in desc:
                    if pattern.search(word) == None:
                        continue
                    else:
                        count = count + 1
                output.write(line)
                output.write('\t')
                output.write(str(count))
                output.write('\n')

def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/bugReport/firefoxIOS_1.txt"
    outfile = "./firefoxIOS_description.txt"
    outfile_2 = "./firefoxIOS_description_size.txt"
    extract_description(filename, outfile)
    compute_description_size(outfile, outfile_2)


if __name__ == "__main__":
    main()
