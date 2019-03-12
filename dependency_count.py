import time
import pyhanlp
from collections import Counter
import multiprocessing
from multiprocessing import Pool
import pyodbc
# from pathos.pools import ProcessPool
from preprocessing import *
from nlpir import *
import numpy as np
import pandas as pd
import os
from prerocessing_2 import *
from Preprocessing_Stage_One import *
import sys


def dependency_analysis(sentence, tar_index, name_index):
    """to analyse the dependency relationship of sentence in a sentences list
    :type tar_index: int; the index of sentences in a document
    :type sentence: string

    """
    import pyhanlp
    import pyodbc
    from collections import Counter

    # to parse sentence
    if 1 < len(sentence) < 200:
        sentence_n = pyhanlp.HanLP.parseDependency(sentence)
        relation_list = []
        for word in sentence_n.iterator():  # 通过dir()可以查看sentence的方法
            relation_list.append(word.DEPREL)
        counter = Counter(relation_list)
        if counter:
            # to record index of sentence
            sen_index = tar_index

            # to record relation results
            keys = []
            values = []
            for key, value in counter.items():
                keys.append(key)
                values.append(value)

            # to find feature name
            keys.append('sen_index')
            keys.append('name_index')
            key_t = ','.join(keys)

            # to find corresponding value
            values.append(sen_index)
            values.append(name_index)
            value_w = [str(value) for value in values]
            value_t = ','.join(value_w)

            # to call sql and save values
            cnxn = pyodbc.connect(
                r'Driver={SQL Server};Server=.\SQLEXPRESS;Database=Statistics_writing_style;Trusted_Connection=yes;')
            cursor = cnxn.cursor()
            # operation1 = "insert Test(sen_index) values (" + str(sen_index) + ")"
            # cursor.execute(operation1)
            operation2 = "insert depen_relation(" + key_t + ") values(" + value_t + ')'
            cursor.execute(operation2)
            #cursor.execute("SELECT 定中关系,并列关系 from depen_relation")
            #while 1:
                #row = cursor.fetchone()
                #if not row:
                    #break
            print("Successfully added into sql server!")
            cnxn.commit()
            cur = cnxn.cursor()
            cnxn.close()
        else:
            print('Name_index: %s, Sen_index:%s: Parsing failed!' % (name_index, tar_index))
            pass
    else:
        pass


if __name__ == '__main__':
    import pyhanlp
    # to collect txt files by person
    import os
    path = 'F:/final' + '/'
    name_list = os.listdir(path)
    print(name_list)

    for j in range(34, 53):
        if j <= 53:
            start = time.time()
            txt = parse_file(path + str(name_list[j]) + '/all.txt')
            # to parse dependency relations
            sentences = txt.split('。')
            print('--> %s sentences splited.'% len(sentences))
            for i in range(len(sentences)):
                dependency_analysis(sentences[i], i, j)
            end = time.time()
            times = end - start
            print("For %s, Done! %d sentences costs -----> %ss." % (name_list[j], len(sentences), times))
        else:
            sys.exit()

