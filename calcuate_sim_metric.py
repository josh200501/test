#!/usr/bin/python
#encoding:utf8
import json
import operator
from numpy import zeros

beha_set_train = []
beha_set_test = []

def load_beha_train_data():
    global beha_set_train
    resfile = "train.log"
    fp = file(resfile, 'r')
    while True:
        line = fp.readline()
        if line:
            cont = json.loads(line)
            beha_set_train.append(cont)
        else:
            break
    fp.close()

def load_beha_test_data():
    global beha_set_test
    resfile = "test.log"
    fp = file(resfile, 'r')
    while True:
        line = fp.readline()
        if line:
            cont = json.loads(line)
            beha_set_test.append(cont)
        else:
            break
    fp.close()

def display_beha_set_info():
    global beha_set_train
    global beha_set_test
    beha_types_train = []
    beha_types_test = []

    print 'training set info:'
    for i in beha_set_train:
        if i['label'] not in beha_types_train:
            beha_types_train.append(i['label'])
    print "total: %d" %(len(beha_set_train))
    print "labels: ", beha_types_train

    print 'testing set info:'
    for i in beha_set_test:
        if i['label'] not in beha_types_test:
            beha_types_test.append(i['label'])
    print "total: %d" %(len(beha_set_test))
    print "labels: ", beha_types_test

def lcs(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    len_base = min(len_str1, len_str2)
    res = zeros((len_str1+1, len_str2+1))

    for i in range(len_str1):
        for j in range(len_str2):
            if str1[i] == str2[j]:
                res[i+1, j+1] = res[i][j] + 1
            else:
                if res[i, j+1] >= res[i+1, j]:
                    res[i+1, j+1] = res[i, j+1]
                else:
                    res[i+1, j+1] = res[i+1, j]

    len_of_lcs = res[len_str1, len_str2]
    #ratio = len_of_lcs*1.0/len_base
    ratio = len_of_lcs*1.0/len_str1
    #print 'LCS: %d match ratio: %.2f' %(len_of_lcs, ratio)
    return ratio

def compare(beha1, beha2):
    """
    beha1: {"BA_1":0, "BA_2":1, xxx}
    beha2: {"BA_1":0, "BA_2":1, xxx}
    return: float num in [0,1]
    """
    sum_count = 0
    inter_count = 0
    res = 0.0
    for i in beha1:
        if beha1[i] != 0 or beha2[i] != 0:
            sum_count += 1
        if beha1[i] != 0 and beha2[i] != 0:
            inter_count += 1
    try:
        res = inter_count * 1.0 / sum_count
    except Exception, e:
        print e
    return res

def find_most_freq(cont_list):
    """
    cont_list: [{'dst_hash':xxx, 'label':xxx, 'score':xx}, xxx]
    return: {'label':xxx, 'freq':xxx, 'cand':{'dst_hash':xxx, 'label':xxx, 'score':xx}}
    """
    res = {}
    for i in cont_list:
        if i['label'] not in res:
            res[i['label']] = 1
        else:
            res[i['label']] += 1

    new = sorted(res.items(), key=lambda d:d[1], reverse=True)
    adopt_type, freq = new[0]
    #print 'most frequent type: %s, freq: %d/%d' %(adopt_type, freq, len(cont_list))

    cont_list_new = []
    for j in cont_list:
        if j['label'] == adopt_type:
            cont_list_new.append(j)

    cont_list_new = sorted(cont_list_new, key=operator.itemgetter('score'), reverse=True)
    #print 'match dst: ', cont_list[0]
    return {'label': adopt_type, 'freq':freq, 'cand':cont_list_new[0]}

def process_one_sample(beha, k):
    """
    beha: {'BA_1':1, 'BA_2':0, xxx}
    k: integer number no less than 1
    return: calculate type
    """
    global beha_set_train
    comp_res = []
    res = 0

    for i in beha_set_train:
        tmp = {}
        res = lcs(beha, i['beha'])
        tmp['dst_hash'] = i['hash']
        tmp['label'] = i['label']
        tmp['score'] = round(res, 2)
        comp_res.append(tmp)

    new = sorted(comp_res, key=operator.itemgetter('score'), reverse=True)

    'get k candidates'
    cand = new[:k]

    'find the most frequent label'
    res_type = find_most_freq(cand)

    return res_type

def choose_beha_pair():
    global beha_set
    match = 'X'
    correct_num = 0
    base_num = 0
    while True:
        count = 0
        if len(beha_set) == 1:
            break
        for i in range(len(beha_set)-1):
            score = compare(beha_set[0]['beha'], beha_set[i+1]['beha'])
            if score > 0.75:
                count += 1
                base_num += 1
                match = 'V'
                print "[%s] hash1: %s label1: %s hash2: %s label2: %s score: %f" %(match, beha_set[0]['hash'], beha_set[0]['label'], beha_set[i+1]['hash'], beha_set[i+1]['label'], score)
                if beha_set[0]['label'] == beha_set[i+1]['label']:
                    correct_num += 1
            else:
                match = 'X'
            #print "[%s] hash1: %s label1: %s hash2: %s label2: %s score: %f" %(match, beha_set[0]['hash'], beha_set[0]['label'], beha_set[i+1]['hash'], beha_set[i+1]['label'], score)
        #print "total matchs: %d" %(count)
        beha_set.remove(beha_set[0])
    print "total match: %d, correct: %d, correct ratio: %f" %(base_num, correct_num, correct_num*1.0/base_num)

if __name__ == '__main__':
    load_beha_train_data()
    load_beha_test_data()
    display_beha_set_info()

    correct_count = 0
    test_count = 0
    #sample = beha_set_test[2]

    for i in beha_set_test:
        test_count += 1
        #print 'sample label: %s' %(sample['label'])
        res = process_one_sample(i['beha'], 1)
        print 'test label: %s, calc label: %s, details: %s' %(i['label'], res['label'], res)
        if i['label'] == res['label']:
            correct_count += 1
        else:
            #print 'test label: %s, test hash: %s, calc label: %s, details: %s' %(i['label'], i['hash'], res['label'], res)
            pass
    print 'test result: total test: %d, correct: %d, precise: %.2f' %(test_count, correct_count, correct_count*1.0/test_count)

