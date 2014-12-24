#!/usr/local/bin/python
#coding:utf8

import os
import sys
from numpy import *
from matplotlib import pyplot as plt

sys.setrecursionlimit(10000)

#str1 = 'backdoor.generic/seq1.log'
#str2 = 'backdoor.generic/seq2.log'
#str1 = 'test_logs/seq1.log'
#str2 = 'test_logs/seq6.log'

#src = 'backdoor.ircbot/seq1.log'
#dst = ['backdoor.ircbot/seq2.log', 'backdoor.ircbot/seq3.log', 'backdoor.ircbot/seq4.log', 'backdoor.ircbot/seq5.log']

src = 'test_logs/seq1.log'
dst = ['test_logs/seq2.log', 'test_logs/seq3.log', 'test_logs/seq4.log', 'test_logs/seq5.log', 'test_logs/seq6.log']

LEFT_UP = 9
LEFT = 8
UP = 7

#x = 'acgbfhk'
#y = 'cegefkh'

#x = ['a','d','e','f','g','h','j','k','l','m','n','j','p','a','x','r','s','b','k','e']
#y = ['a','b','e','k','g','h','i','j','k','m','n','o','p','q','r','s','t']

def load_data(log_file):
    res = []

    fp = open(log_file, 'r')
    conts = fp.readlines()
    fp.close()

    for i in conts:
        res.append(i.strip())

    return res


class LCS():
    def __init__(self, str1, str2):
        self.str1 = str1
        self.str2 = str2
        self.len_str1 = len(str1)
        self.len_str2 = len(str2)
        self.len_base = min(self.len_str1, self.len_str2)
        self.res = zeros((self.len_str1+1, self.len_str2+1))
        self.flag = zeros((self.len_str1+1, self.len_str2+1))
        self.sub_seq_x = []
        self.sub_seq_y = []

    def lcs(self):
        for i in range(self.len_str1):
            for j in range(self.len_str2):
                if self.str1[i] == self.str2[j]:
                    self.res[i+1, j+1] = self.res[i][j] + 1
                    self.flag[i+1, j+1] = LEFT_UP
                else:
                    if self.res[i, j+1] >= self.res[i+1, j]:
                        self.res[i+1, j+1] = self.res[i, j+1]
                        self.flag[i+1, j+1] = LEFT
                    else:
                        self.res[i+1, j+1] = self.res[i+1, j]
                        self.flag[i+1, j+1] = UP

        len_of_lcs = self.res[self.len_str1, self.len_str2]
        ratio = len_of_lcs*1.0/self.len_base
        #print 'LCS: %d match ratio: %.2f' %(len_of_lcs, ratio)
        return (len_of_lcs, ratio)

    def call_sub_seq(self):
        self.lcs_sub_seq(self.len_str1, self.len_str2)

    def lcs_sub_seq(self, i, j):
        if i == 0 or j == 0:
            return
        if self.flag[i,j] == LEFT_UP:
            #print '%s, [%d,%d]' %(self.str2[j-1], i-1, j-1)
            self.sub_seq_x.append(i-1)
            self.sub_seq_y.append(j-1)
            #bk_y.append(j-1)
            self.lcs_sub_seq(i-1, j-1)
        else:
            if self.flag[i,j] == UP:
                self.lcs_sub_seq(i, j-1)
            else:
                self.lcs_sub_seq(i-1, j)

    def draw_sub_seq(self):
        return (self.sub_seq_x, self.sub_seq_y)
        #plt.plot(self.sub_seq_x, self.sub_seq_y)
        #plt.show()

    def lcs_continue(self):
        max_len = 0
        pos = 0
        res = [0]*(self.len_str2+1)
        for i in range(self.len_str1):
            for j in range(self.len_str2):
                if self.str1[i] == self.str2[self.len_str2-1-j]:
                    res[self.len_str2-j] = res[self.len_str2-1-j] + 1
                    if res[self.len_str2-j] > max_len:
                        max_len = res[self.len_str2-j]
                        pos = self.len_str2-1-j
                else:
                    res[self.len_str2-j] = 0
        #print 'max length of subsequence: %d' %(max_len)

        sub_seq = [0]*max_len
        for i in range(max_len):
            sub_seq[i] = self.str2[pos-max_len+1+i]
        #print sub_seq


if __name__ == '__main__':
    "self test ..."
    """
    x = 'acgbfhk'
    y = 'cegefkh'
    print 'x:', x
    print 'y:', y
    a = LCS(x,y)
    a.lcs()
    a.call_sub_seq()
    #a.draw_sub_seq()
    #a.lcs_continue()
    """

    plt.figure()
    for i in dst:
        x = load_data(src)
        y = load_data(i)
        a = LCS(x,y)
        a.lcs()
        a.call_sub_seq()
        axis_x, axis_y = a.draw_sub_seq()
        plt.plot(axis_x, axis_y, '.')

    plt.show()


