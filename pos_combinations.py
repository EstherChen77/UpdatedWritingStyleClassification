from preprocessing import parse_file
from itertools import tee, islice
from nltk import ngrams
from collections import Counter
import os
import pandas as pd
import numpy as np
import time
from text_preprocessing import remove_punc

def isplit(source, sep):
    sepsize = len(sep)
    start = 0
    while True:
        idx = source.find(sep, start)
        if idx == -1: #相当于break了
            yield source[start:]
            return
        yield source[start:idx]
        start = idx + sepsize

def pairwise(iterable, n=2):
    return zip(*(islice(it, pos, None) for pos, it in enumerate(tee(iterable, n))))


def yield_triple_list(content, n):
    """ to yield n-grams in a document by every sentence"""
    sentences  = isplit(content,".")
    for sentence in sentences:
        all_ngram = ngrams(isplit(sentence," "), n)
        for word in all_ngram:
            yield word

def mklbl(prefix, n):
    return ["%s%s" % (prefix, i) for i in range(n)]


def mkltl(prefix, m, n):
    return ["%s%s" % (prefix, i) for i in range(m, n)]


if __name__ == '__main__':
    path = 'F:/by_gene/'
    file_list = os.listdir(path)
    gene_list = [gene.replace(".txt", "") for gene in file_list]

# to creat a dataframe
    miindex = pd.MultiIndex.from_product([gene_list, mkltl("", 2, 6)])
    micolumns = pd.MultiIndex.from_tuples(
        [("1", "combination"), ("2", "combination"), ("3", "combination"), ("4", "combination"), ("5", "combination"),
         ("6", "combination"), ("7", "combination"),
         ("1", "frequency"), ("2", "frequency"), ("3", "frequency"), ("4", "frequency"), ("5", "frequency"),
         ("6", "frequency"), ("7", "frequency")])
    dfmi = pd.DataFrame(np.arange(len(miindex) * len(micolumns)).reshape((len(miindex), len(micolumns))), index=miindex,
                        columns=micolumns).sort_index().sort_index(axis=1)

# to count n-grams
    start = time.time()
    for j in range(len(gene_list)):
        file = path + str(gene_list[j]) + ".txt"
        content = parse_file(file)
        if len(content) < 100:
            raise FileExistsError
        else:
            punc  = ["[","]","'",","]
            for p in punc:
                txt = content.replace(p,"")
            print(len(txt))
        if len(txt) > 100:
            for n in range(2,6):
                count = Counter(yield_triple_list(txt,n))
                most_common = count.most_common(7)
                # to update value in dataframe
                idx = pd.IndexSlice
                cap = len(most_common)
                for i in range(1,cap):
                    replace = "+".join(most_common[i][0])
                    dfmi.loc[idx[str(gene_list[j]), str(n)], idx[str(i), 'combination']] = replace
                    dfmi.loc[idx[str(gene_list[j]), str(n)], idx[str(i), 'frequency']] = most_common[i][1]
        else:
            print("No string content got!")
    end = time.time()
    print("Done! ---> %ss spent!"% (end-start))

# to save as .xlsx
    file_path = r'E:/Ipython/Machine Learning/research/by_gene_pos_ngrams.xlsx'
    writer = pd.ExcelWriter(file_path)
    dfmi.to_excel(writer, index=True, encoding='utf-8', sheet_name='pos_ngrams')
    writer.save()
    print("Successfully Saved!")
