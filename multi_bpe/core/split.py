#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 10:23:00 2019

@author: daniel
"""
"""

"""
import io
filelength = 0

with open('../dataset/clean_dataset.txt', 'r', encoding = "utf-8") as f:
    lines = f.readlines()
    filelength = len(lines)
    print(filelength)
    count = int(filelength / 100)
    for i in range(100):
        splitpath = '../data/splited_file/splited_{}.txt'.format(i)
        strcount = ''
        for j in range(i*count, (i+1)*count, 1):
            strcount = strcount + lines[j]
        with open(splitpath, 'w', encoding = "utf-8") as fw:
            fw.write(strcount)
            strcount = ''
