# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 20:44:54 2019

@author: IVPL-D11
"""

import csv
import math

activityID = []

with open('activityLabel.csv', 'rt') as f:
    reader = csv.reader(f)
    # read file row by row
    for row in reader:
        activityID.append(row[0])
    del activityID[-1]

for j in range(0,len(activityID)):
    writefilename = activityID[j]+'_test.csv'
    readfilename = activityID[j]+'.csv'
    with open(writefilename, 'wt', newline="") as testfile:
        csv_writer = csv.writer(testfile)
        # open file
        with open(readfilename, 'rt') as f: 
            reader = csv.reader(f)
            # read file row by row
            i = 0
            tmp = []
            for row in reader:
                try:
                    i+=1
                    tmp.append(row[0])
                    tmp.append(row[1])
                    tmp.append(row[2])
                    if(i == 15):
                        csv_writer.writerow(tmp)
                        tmp = []
                        i = 0
                except:
                    print("Reached file end: ".readfilename)
                