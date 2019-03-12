from preprocessing import *
from nlpir import *
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import sys
from collections import Counter


# to set pos tagging origin
SetPOSmap(2)
f = open("F:/paperdownload/G25.txt",'r',encoding='utf-8',errors="surrogateescape")
for word in f.readlines():
    AddUserWord(word.encode('UTF8')+b'\t'+b'n')


def average(count_list):
    """to calculate average value of a certain pos in a document"""
    av_value = np.mean(count_list)
    return av_value


def pos_statistic(pos_li, t_pos):
    """to count target pos in every sentence"""
    c = 0
    for p in pos_li:
        for j in range(len(t_pos)):
            if p == t_pos[j]:
                c += 1
        return c


def isplit(source, sep):
    sepsize = len(sep)
    start = 0
    while True:
        idx = source.find(sep, start)
        if idx == -1:
            yield source[start:]
            return
        yield source[start:idx+1]
        start = idx + sepsize


def flatten(llist):
    for item in llist:
        for word in item:
            yield word
    return word


def fetch_string(iterator):
    text = ""
    for string in flatten(iterator):
        text = text + str(string)
    return text


# to pre_process txt files
path = 'F:/final' + '/'
name_list = os.listdir(path)

sen_count = []
words_per_sen = []
pos_a = []
pos_v = []
pos_d = []
pos_n = []
pos_e = []
pos_i = []
percentages = []

for name in name_list:
    content = parse_file(path + str(name) + '/all.txt')
    # to seg sentences and record how many sentences
    sentences = [sentence for sentence in isplit(content, '。')]
    print('There are %d sentences in %s.txt file' % (len(sentences), name))
    sen_count.append(len(sentences))
    # to seg words in every sentence

    vc_list = []
    ac_list = []
    nc_list = []
    dc_list = []
    ic_list = []
    ec_list = []
    words = []
    pos_final = []
    word_length = []

    for sentence in sentences:
        p = sentence
        p = p.encode('UTF8')
        pos_list = []
        words_list = []
        word_length_list = []
        # to record how many non_punc words in a sentence
        for t in Seg(p):
            pos_list.append(t[1])
            words_list.append(t[0])
            word_length_list.append(len(t[0]))

        pos_list.append(".")
        word_length_list.append(".")

        count = 0
        for pos in pos_list:
            if pos != 'w' and 'un' and 'x':
                count += 1

        words.append(count)

        # to record every pos in a sentence
        s = pos_list

        v_pos = ['v', 'vg', 'vd', 'vn']
        vc = 0
        for p in v_pos:
            for v in s:
                if v == p:
                    vc += 1
        vc_list.append(vc)

        n_pos = ['n', 'nr', 'ns', 'nt', 'nz']
        nc = 0
        for p in n_pos:
            for v in s:
                if v == p:
                    nc += 1
        nc_list.append(nc)

        a_pos = ['Ag', 'a', 'ad', 'an']
        ac = 0
        for p in a_pos:
            for v in s:
                if v == p:
                    ac += 1
        ac_list.append(ac)

        d_pos = ['d', 'g']
        dc = 0
        for p in d_pos:
            for v in s:
                if v == p:
                    dc += 1
        dc_list.append(dc)

        i_pos = ['i']
        ic = 0
        for p in i_pos:
            for v in s:
                if v == p:
                    ic += 1
        ic_list.append(ic)

        e_pos = ['e', 'y', 'o']
        ec = 0
        for p in v_pos:
            for v in s:
                if v == p:
                    ec += 1
        ec_list.append(ec)
        pos_final.append(pos_list)
        word_length.append(word_length_list)

    words_f = np.mean(words)
    av_vc = sum([i for i in vc_list if i != 0 and max(vc_list)])/len([i for i in vc_list if i != 0 and max(vc_list)])
    av_nc = sum([i for i in nc_list if i != 0 and max(nc_list)])/len([i for i in nc_list if i != 0 and max(nc_list)])
    av_ac = sum([i for i in ac_list if i != 0 and max(ac_list)])/len([i for i in ac_list if i != 0 and max(ac_list)])
    av_dc = sum([i for i in dc_list if i != 0 and max(dc_list)])/len([i for i in dc_list if i != 0 and max(dc_list)])
    av_ec = sum([i for i in ec_list if i != 0 and max(ec_list)])/len([i for i in ec_list if i != 0 and max(ec_list)])

    # to record every gene
    pos_a.append(av_ac)
    pos_v.append(av_vc)
    pos_d.append(av_dc)
    pos_n.append(av_nc)
    pos_e.append(av_ec)
    words_per_sen.append(words_f)


df = pd.DataFrame(columns=("name", "sen_count", "words_per_sen", "pos_v", "pos_d", "pos_a", "pos_n", "pos_e"))
df['name'] = name_list
df['sen_count'] = np.array(sen_count)
df['words_per_sen'] = np.array(words_per_sen)
df['pos_a'] = np.array(pos_a)
df['pos_v'] = np.array(pos_v)
df['pos_d'] = np.array(pos_d)
df['pos_n'] = np.array(pos_n)
df['pos_e'] = np.array(pos_e)


file_path = r'E:/Ipython/Machine Learning/research/nc_statistics.xlsx'
writer = pd.ExcelWriter(file_path)
df.to_excel(writer, index=True, encoding='utf-8', sheet_name='new_statistics')
writer.save()



'''
    with open(path + str(name) + '/pos.txt', 'wb') as fo:
        fo.write(pos_content.encode('utf-8', errors="surrogateescape"))
        fo.close()
    '''
'''
    with open(path + str(name) + '/word_length.txt', 'wb') as fo:
        fo.write(word_length_content.encode('utf-8', errors="surrogateescape"))
        fo.close()
'''

    #print("%s pos data.txt saved!" % name)

'''    percen = [dc_list[i] / words[i] for i in range(len(dc_list))]
    print(len(percen))
    # to sum all to calculate average value
    print(len(dc_list))
    print(len([i for i in dc_list if i==0]))
    sortdata = sorted(dc_list, reverse=False)
    print(sortdata)

    co = Counter(sortdata)
    item = np.unique(sortdata)
    a = list(co)
    b = list(co.values())

    x = sorted(percen)
    ca = Counter(x)
    item = np.unique(sortdata)
    newa = list(ca)
    percen = list(ca.values())

    oo = {"pos_count": newa, "percen": percen}
    df = pd.DataFrame(oo)
    print(df)
    plt.plot(df["pos_count"], df["percen"])
    plt.show()
    sys.exit()

    c = {"pos_count":a, "freqency":b, "percen":percen}
    df = pd.DataFrame(c)
    print(df)
    plt.plot(df["pos_count"],df["percen"])
    plt.show()
'''

'''
    # to write pos result in
    pos_content = fetch_string(pos_final)
    word_length_content = fetch_string(word_length)
'''