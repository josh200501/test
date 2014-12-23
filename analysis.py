#!/usr/local/bin/python
# -*- coding: utf8 -*-
import mongodb
import sys_info
import os
import json

beha_seq = []

def get_sample_label(hashvalue):
    db = mongodb.connect_readonly()
    collection = db.queue_xp
    res = collection.find_one(
            {"hashvalue": hashvalue},\
                    {"_id":0, "type_beha":1}
            )
    if res:
        tmp = res['type_beha']
        if '!' in tmp:
            tmp = tmp.split('!')[0]
        return tmp
    else:
        return 'unknow'

def get_beha_seqs_from_local(log_file):
    global beha_seq
    filt_dup = True
    exp_list = ['REG_getval', 'REG_openkey', 'FILE_open']

    pcap_file = ''
    ss_file = ''
    str_file = ''
    hashvalue = ''

    data = mongodb.pack(log_file, pcap_file, ss_file, str_file, hashvalue)
    lines = data['contents']['actionlist']
    if lines == "":
        return False

    for line in lines:
        action = line['action']
        if action in exp_list:
            continue

        if not filt_dup:
            beha_seq.append(action)
            continue

        if not beha_seq:
            beha_seq.append(action)
            continue
        if action == beha_seq[-1]:
            pass
        else:
            beha_seq.append(action)
    return True

def get_beha_seqs_from_db(hashvalue):
    global beha_seq
    filt_dup = False
    exp_list = ['REG_getval', 'REG_openkey', 'FILE_open']

    beha_seq = []
    lines , pcap_file, static_info, ss, sstr, ana_time, ana_res_db = sys_info.read_log(hashvalue)
    if lines == "":
        return False

    for line in lines:
        action = line['action']
        if action in exp_list:
            continue

        if not filt_dup:
            beha_seq.append(action)
            continue

        if not beha_seq:
            beha_seq.append(action)
            continue
        if action == beha_seq[-1]:
            pass
        else:
            beha_seq.append(action)
    return True

def get_hashvalue_from_db():
    db = mongodb.connect_readonly()
    collection = db.status
    res = []
    cur = collection.find(
            {"process_status":"6","ana_res":""},\
                    {"_id":0, "hashvalue":1})
    length = cur.count()
    for i in range(length):
        tmp = cur.next()
        print tmp
        res.append(tmp['hashvalue'])
    return res

def get_hashvalue_from_local(file_path):
    hash_cont = []
    #hash_file = 'hashvalues.log'
    hash_file = file_path
    fp = file(hash_file, 'r')
    while True:
        line = fp.readline()
        if line:
            hash_cont.append(line.strip())
        else:
            break
    fp.close()
    return hash_cont

def main(hash_file, res_file):
    newline = os.linesep
    fp = file(res_file,'w')
    hashvalues = get_hashvalue_from_local(hash_file)
    #hashvalues = get_hashvalue_from_db()

    if len(hashvalues) < 1:
        print "no hashvalue returned."
        exit()
    print "length of hashvlues: ", len(hashvalues)

    j = 0
    for i in hashvalues:
        j += 1
        get_beha_seqs_from_db(i)
        len_beha_seq = len(beha_seq)
        if len(beha_seq)< 1:
            continue
        label = get_sample_label(i)
        item = {"hash":i, "beha":beha_seq, "label":label}
        store_item = json.dumps(item)
        fp.write(store_item)
        fp.write(newline)
        print "[%d] hash: %s, len of beha seq: %s" %(j, i, len_beha_seq)
    fp.close()

if __name__ == '__main__':
    """
    hashvalues = get_hashvalue_from_local()
    for i in range(len(hashvalues)):
        print "[%d]: hash: %s label: %s" %(i, hashvalues[i], get_sample_label(hashvalues[i]))
    """
    #main('hashs_train.log', 'train.log')
    #main('hashs_test.log', 'test.log')
    #logfile = '../logs/050d904ed1a5fb64970030e13f38bf5d9d1eb205.log'
    #logfile = '../logs/4f200b98079e8f42cf1664cbdf305e735c6bcd6c.log'
    #logfile = '../logs/1fcc16fbd9583df9a85dbc0133748f97ab69c8a1.log'
    #logfile = '../logs/2b64394ae66aeee986234a301535c1406a7c3907.log'
    #logfile = '../logs/30653a5087b07bcfc9bc3405ea6115deacf846bd.log'
    #logfile = '../logs/6d874471b36e0eae89204217e2c68a99f3f7a201.log'
    """
    the follows are typed samples
    """
    #logfile = '../Backdoor.IRCbot/38974776656ab7284caa13ce991b1fd0fb3c0039.log'
    #logfile = '../Backdoor.IRCbot/419c906365fefdbaf37241616c94544c073d6dd7.log'
    #logfile = '../Backdoor.IRCbot/44b4b2ca6aabd089170a7cc818a5cdcda1fbef58.log'
    #logfile = '../Backdoor.IRCbot/55dd2144bcf85caf696a77e36d3e68a2397e0a16.log'
    #logfile = '../Backdoor.IRCbot/8728eb0f5c6a5403e9de1ee280b009cd63ce92a7.log'

    #logfile = '../Backdoor.Generic/91b15046e499d7b8c25d2c5a1fe48464147487a4.log'
    logfile = '../Backdoor.Generic/a4ffeeb95604fe0fb00c8393aacea59829dccc63.log'

    res = get_beha_seqs_from_local(logfile)
    if not res:
        print 'log is empty'
    j = 0
    for i in beha_seq:
        j += 1
        print i
    #main('hashs_train.log','train.log')
    #main('hashs_test.log','test.log')

