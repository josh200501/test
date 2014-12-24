#!/usr/local/bin/python
#coding:utf8
import sys

sys.setrecursionlimit(10000)

from numpy import *
from matplotlib import pyplot as plt

import os

linesep = os.linesep

x = []
y = []

bk_x = []
bk_y = []

str1 = 'seq4.log'
str2 = 'seq5.log'

#str1 = 'backdoor.generic/seq1.log'
#str2 = 'backdoor.generic/seq2.log'
#str1 = 'test_logs/seq1.log'
#str2 = 'test_logs/seq6.log'
str1 = 'backdoor.ircbot/seq1.log'
str2 = 'backdoor.ircbot/seq5.log'

print '%s vs %s' %(str1, str2)

fp1 = open(str1, 'r')
fp2 = open(str2, 'r')
conts1 = fp1.readlines()
conts2 = fp2.readlines()

fp1.close()
fp2.close()

for i in conts1:
    x.append(i.strip())

for i in conts2:
    y.append(i.strip())

#x = 'acgbfhk'
#y = 'cegefkh'

len_str1 = len(x)
len_str2 = len(y)

len_base = min(len_str1, len_str2)

res = zeros((len_str1+1, len_str2+1))
flag = zeros((len_str1+1, len_str2+1))

LEFT_UP = 9
LEFT = 8
UP = 7

#x = ['a','d','e','f','g','h','j','k','l','m','n','j','p','a','x','r','s','b','k','e']
#y = ['a','b','e','k','g','h','i','j','k','m','n','o','p','q','r','s','t']
"""
x_long = len(x)
y_long = len(y)

res_x = []
res_y = []

res = zeros((x_long, y_long))

for i in range(x_long):
    for j in range(y_long):
        if x[i] == y[j]:
            res[i][j] = 1
            res_x.append(i)
            res_y.append(j)

#print res
plt.plot(res_x,res_y, '*')
plt.show()
"""

def LCS(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
#    res = zeros((len_str1, len_str2))
#    flag = zeros((len_str1, len_str2))
    global res,flag, len_base

    for i in range(len_str1):
        for j in range(len_str2):
            if str1[i] == str2[j]:
                res[i+1, j+1] = res[i][j] + 1
                flag[i+1, j+1] = LEFT_UP
            else:
                if res[i, j+1] >= res[i+1, j]:
                    res[i+1, j+1] = res[i, j+1]
                    flag[i+1, j+1] = LEFT
                else:
                    res[i+1, j+1] = res[i+1, j]
                    flag[i+1, j+1] = UP

    len_of_lcs = res[len_str1, len_str2]
    ratio = len_of_lcs*1.0/len_base

    print 'LCS: %d match ratio: %.2f' %(len_of_lcs, ratio)

def lcs_continue(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    max_len = 0
    pos = 0
    res = [0]*(len_str2+1)
    for i in range(len_str1):
        for j in range(len_str2):
            if str1[i] == str2[len_str2-1-j]:
                res[len_str2-j] = res[len_str2-1-j] + 1
                if res[len_str2-j] > max_len:
                    max_len = res[len_str2-j]
                    pos = len_str2-1-j
            else:
                res[len_str2-j] = 0
    print 'max length of subsequence: %d' %(max_len)

    sub_seq = [0]*max_len
    for i in range(max_len):
        sub_seq[i] = str2[pos-max_len+1+i]
    print sub_seq

def sub_seq(i, j):
    global bk_x, bk_y
    if i == 0 or j == 0:
        return

    if flag[i,j] == LEFT_UP:
        print '%s, [%d,%d]' %(y[j-1], i-1, j-1)
        bk_x.append(i-1)
        bk_y.append(j-1)
        sub_seq(i-1, j-1)
    else:
        if flag[i,j] == UP:
            sub_seq(i, j-1)
        else:
            sub_seq(i-1, j)

if __name__ == '__main__':
    LCS(x,y)
    #lcs_continue(x,y)
    sub_seq(len_str1, len_str2)
    plt.plot(bk_x, bk_y, 'o')
    plt.show()


