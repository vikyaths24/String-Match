# -*- coding: utf-8 -*-
"""2357897779_efficient

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1h2yvrncf8DJMSzaOj2OXR1qJJJju_wy1
"""
import sys
import time
start_time = time.time()
import sys
import pdb
import argparse
import numpy as np
import copy
import re
import unittest
import csv
import psutil
import tracemalloc
gap=30
tracemalloc.start()
align=np.zeros((4,4))
align[0][0]=0
align[0][1]=110
align[0][2]=48
align[0][3]=94
align[1][2]=118
align[1][3]=48
align[2][3]=110
align=align+align.T
print(align)
costl=0

def corres(x):
  if x=='A':
    return 0
  if x=='C':
    return 1
  if x=='G':
    return 2
  if x=='T':
    return 3
def lastLineAlign(x, y):
  
  global gap
  global align
  row = y
  column = x 
  minLen = len(y)
  prev = [0 for i in range(minLen + 1)]
  current = [0 for i in range(minLen + 1)]


  for i in range(1, minLen + 1):
    prev[i] = prev[i-1]+gap
  
  current[0] = 0
  for j in range(1, len(column) + 1):
    current[0] += gap
    l1=corres(x[j-1])
    for i in range(1, minLen + 1):
      l2=corres(y[i-1])
      
      current[i] = min(current[i-1] + gap, prev[i-1] + align[l1][l2], prev[i] + gap)
    prev = copy.deepcopy(current) 

  return current 

def partitionY(scoreL, scoreR):
  max_index = 0
  max_sum = float('Inf')
  for i, (l, r) in enumerate(zip(scoreL, scoreR[::-1])):
    
    if sum([l, r]) < max_sum:
      max_sum = sum([l, r])
      max_index = i
  return max_index 

def dynamicProgramming(x, y):
  global gap
  global align 
  
  M = np.zeros((len(x) + 1, len(y) + 1))
  Path = np.empty((len(x) + 1, len(y) + 1), dtype=object)

  for i in range(1, len(y) + 1):
    M[0][i] = M[0][i-1] + gap
    Path[0][i] = "l"
  for j in range(1, len(x) + 1):
    M[j][0] = M[j-1][0] + gap
    Path[j][0] = "u"
  
  for i in range(1, len(x) + 1):
    l1=corres(x[i-1])
    for j in range(1, len(y) + 1):
      l2=corres(y[j-1])
      if x[i-1] == y[j-1]:
        M[i][j] = min(M[i-1][j-1] + align[l1][l2], M[i-1][j] + gap, M[i][j-1] + gap)
        if M[i][j] == M[i-1][j-1] + align[l1][l2]:
          Path[i][j] =  "d"
        elif M[i][j] == M[i][j-1] + gap:
          Path[i][j] = "l"
        else:
          Path[i][j] = "u"
      else:
        M[i][j] = min(M[i-1][j-1] + align[l1][l2], M[i-1][j] + gap, M[i][j-1] + gap)
        if M[i][j] == M[i-1][j-1] + align[l1][l2]:
          Path[i][j] =  "d"
        elif M[i][j] == M[i][j-1] + gap:
          Path[i][j] = "l"
        else:
          Path[i][j] = "u"

  row = []
  column= []
  middle = []
  i = len(x)
  j = len(y)
  cost=M[len(x)][len(y)]
  while Path[i][j]:
    if Path[i][j] == "d":
      row.insert(0, y[j-1])
      column.insert(0, x[i-1])
      if x[i-1] == y[j-1]:
        middle.insert(0, '|')
      else:
        middle.insert(0, ':')
      i -= 1
      j -= 1
    elif Path[i][j] == "u":
      row.insert(0, '_')
      column.insert(0, x[i-1])
      middle.insert(0, 'x')
      i -= 1
    elif Path[i][j] == "l":
      column.insert(0, '_')
      row.insert(0, y[j-1])
      middle.insert(0, 'x')
      j -= 1

  return cost,row, column, middle


def dandc(x, y):
  row = ""
  column = ""
  middle = ""
  cost=0
  global costl
  if len(x) == 0 or len(y) == 0:
    if len(x) == 0:
      column = '_' * len(y)
      row = y
      middle =  'x' * len(y)
      cost=len(y)*30
    else:
      column += x
      row += '_' * len(x)
      middle =  'x' * len(x)
      cost=len(x)*30
  elif len(x) == 1 or len(y) == 1:
    cost, row, column, middle = dynamicProgramming(x, y)
    # concatenate into string
    
    row, column, middle = map(lambda x: "".join(x), [row, column, middle]) 
  else:
    xlen = len(x)
    xmid = int(xlen/2)
    ylen = len(y)

    scoreL = lastLineAlign(x[:xmid], y)
    scoreR = lastLineAlign(x[xmid:][::-1], y[::-1])
    ymid = partitionY(scoreL, scoreR)
    c1, row_l, column_u, middle_l = dandc(x[:xmid], y[:ymid])
    c2, row_r, column_d, middle_r = dandc(x[xmid:], y[ymid:])
    row = row_l + row_r
    column = column_u + column_d 
    middle = middle_l + middle_r
    cost=c1+c2
  return cost, row, column, middle
        

def textout(s1,s2,cost):
  f=open("output.txt","w")
    
  f.write(str(s1)+"\n")
  f.write(str(s2)+"\n")
  f.write(str(cost)+"\n")
  
  
  f.write(str(tracemalloc.get_traced_memory()[1] / (1024 ))+"\n")
  f.write(str(time.time() - start_time)+"\n")
  tracemalloc.stop()
  print(tracemalloc.get_traced_memory())



trainimg=[]
with open(str(sys.argv[1])) as csvfile:
  reader = csv.reader(csvfile) # change contents to floats
  for row in reader: # each row is a list
      trainimg.append(row[0])

str1=trainimg[0]
for i in range (1,len(trainimg)):
  l=str(trainimg[i])
  
  if str(trainimg[i]).isnumeric():
    str1=str1[:int(l)+1]+str1+str1[int(l)+1:len(str1)]
    
  else:
    break
str2=trainimg[i]
for k in range (i,len(trainimg)):
  l=str(trainimg[k])
  
  if str(trainimg[k]).isnumeric():
    str2=str2[:int(l)+1]+str2+str2[int(l)+1:len(str2)+1]
    
str1l=list(str1)
str2l=list(str2)

cost,row, column, middle = dandc(str1, str2)
print(cost)

s1=row[:50]+' '+row[-50:]
s2=column[:50]+' '+column[-50:]
print(len(str1))
print(len(str2))
textout(s2,s1,cost)