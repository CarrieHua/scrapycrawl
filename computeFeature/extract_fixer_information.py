#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file fixer_experience.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire bug_id, modified time, fixer name 
# **
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def fixer_experience(filename, outfile):
    """
    input: filename, the file which store the crawled data; 
    outfile: the file contain bug_id, reported time, reporter name
    """
    output = open(outfile, 'w')
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split("\t")
            if len(mid) == 16:
                bug_id = mid[0]
                output.write(bug_id)
                output.write('\t')
                modified_time = mid[11][3:19]
                output.write(modified_time)
                output.write('\t')
                #fixer_name = mid[7][3:len(mid[10])-2]
                fixer_name = mid[7].split("'")[1].split(';')[0]
                output.write(fixer_name)
                output.write('\n')
            
    output.close()


def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/bugReport/firefoxIOS_1.txt"
    outfile = "./firefox_fixer_experience.txt"
    fixer_experience(filename, outfile)


if __name__ == "__main__":
    main()
