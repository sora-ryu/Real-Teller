# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 20:54:22 2019

@author: IVPL-D11
"""

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
    writefilename = activityID[j]+'_features.csv'
    readfilename = activityID[j]+'_test.csv'
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
                    torsox = float(row[24])
                    torsoy = float(row[25])
                    torsoz = float(row[26])
                    neckx = float(row[3])
                    necky = float(row[4])
                    neckz = float(row[5])
                    denom = math.sqrt(math.pow((neckx - torsox),2) + math.pow((necky - torsoy),2) + math.pow((neckz - torsoz),2))
                    tmp = []
                    i = 0
                    while (i < 24):
                        tmp.append((float(row[i]) - torsox)/denom)
                        tmp.append((float(row[i+1]) - torsoy)/denom)
                        tmp.append((float(row[i+2]) - torsoz)/denom)
                        i+=3
                    i = 27
                    while (i < 45):
                        tmp.append((float(row[i]) - torsox)/denom)
                        tmp.append((float(row[i+1]) - torsoy)/denom)
                        tmp.append((float(row[i+2]) - torsoz)/denom)
                        i+=3
                    csv_writer.writerow(tmp)
                except:
                    print("Reached file end: ",readfilename)

                