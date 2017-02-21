#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file compute_fixer_experience.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire fixer experience 
# **
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def compute_reporter_experience(filename, outfile):
    """
    input: filename, the file which store the crawled data; 
    outfile: the file contain bug_id, reported time, reporter name
    """
    output = open(outfile, 'w')
    # a dict which represents fixer_name:[time1, time2 ,...]
    reporters = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            mid = line.split("\t")
            if len(mid) == 3:
                name = mid[2]
                time = mid[1]
                if name not in reporters:
                    reporters[name] = []
                reporters[name].append(time)
    with open(filename) as of:
        for line in of:
            line = line.strip()
            mid = line.split('\t')
            if len(mid) == 3:
                name = mid[2]
                time = mid[1]
                reporters[name].sort()
                count = 0
                for i in range(len(reporters[name])):
                    t = reporters[name][i]
                    if t <= time:
                        count = count + 1
                    else:
                        break
                output.write(line)
                output.write('\t')
                output.write(str(count))
                output.write('\n')
    output.close()


def main():
    """
    main function
    """
    filename = "./firefox_reporter_experience.txt"
    outfile = "./compute_firefox_reporter_experience.txt"
    compute_reporter_experience(filename, outfile)


if __name__ == "__main__":
    main()
