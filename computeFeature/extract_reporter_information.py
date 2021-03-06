#!/usr/bin/python2.7.6
# -*- coding: utf-8 -*-

"""
# **
# * @file fixer_experience.py
# * @author Carrie
# * @date 2017/01/13
# * @brief acquire bug_id, reported time, reporter name 
# **
"""

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def reporter_experience(filename, outfile):
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
                report_time = mid[9][3:19]
                output.write(report_time)
                output.write('\t')
                #reporter_name = mid[10][3:len(mid[10])-2]
                reporter_name = mid[10].split("'")[1]
                output.write(reporter_name)
                output.write('\n')
            
    output.close()


def main():
    """
    main function
    """
    filename = "/home/carrie/scrapyCrawe/bugReport/firefoxIOS_1.txt"
    outfile = "./firefox_reporter_experience.txt"
    reporter_experience(filename, outfile)


if __name__ == "__main__":
    main()
