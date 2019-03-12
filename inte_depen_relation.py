from word_length import *
from nlpir import *
import matplotlib.pyplot as plt
import numpy as np
import time


def match_academic(cuts):
    voca = parse_file("F:/paperdownload/G25.txt")
    amount = 0
    for word in cuts:
        if word in voca:
            amount += 1
    return amount


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

def seg_sen(sentence):
    pos_list = []
    words_list = []
    p = sentence
    p = p.encode('UTF8', errors="surrogateescape")
    for t in Seg(p):
        pos_list.append(t[1])
        words_list.append(t[0])
    return [pos_list, words_list]


def dependency_analysis(sentence, gene, name, paper_index, sen_count,sen_index):
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
        dict = {}
        if counter:
            for key, value in counter.items():
                dict.update({key:value})
            relations = sum(dict.values())
            dict.update({"gene":gene,"name":name,"paper":paper_index,"sentences":sen_count,"sen":sen_index,"relations":relations})
            return dict

        else:
            print('Name_index: %s, Sen_index:%s: Parsing failed!' % (name_index))
            pass
    else:
        pass




def by_sentence(gene,sen,sen_index, name, paper_index, sen_count):
    if len(sen) > 0:
        pack = seg_sen(sen)
        cut_words = pack[1]
        pos_list = pack[0]
        # to match n, v, a, d, e
        pos = Pos(pos_list)
        EachPos = pos.cal_all()
        # to match academic words
        amount = match_academic(cut_words)
        total_words = len(cut_words)
        if total_words > 0:
            proportion = amount / total_words
        else:
            proportion = 0
        dict = {"gene":gene, "name":name, "paper":paper_index, "sentences":sen_count, "sen":sen_index,
                "words":len(cut_words),"aca_count":amount, "aca_pro":proportion, "pos1": EachPos[0],
                "pos2": EachPos[1],"pos3": EachPos[2],"pos4": EachPos[3],"pos5": EachPos[4],"pos6":EachPos[5]}
        return dict
    else:
        pass


if __name__ == '__main__':
    st = time.time()
    dictList = []
    for gene in range(1,8):
        path = 'F:/final/'+str(gene) +'/'
        for name in os.listdir(path):
            file_path = path + name + "/"
            files = len(os.listdir(file_path))
            for file_name in range(files-2):
                print("-" * 30 + "->for %s, this is %s in %s papers" % (name, file_name, files - 3))
                dire = file_path + str(file_name) + ".txt"
                content = parse_file(dire)
                sentences = content.split('。')
                for i in range(len(sentences)):
                    dic = dependency_analysis(sentence=sentences[i],gene=gene,sen_index=i,name = name, paper_index=file_name,sen_count = len(sentences))
                    if dic:
                        dictList.append(dic)

    df = pd.DataFrame(dictList)
    # to save as .xlsx
    file_path = r'E:/Ipython/Machine Learning/research/data/depen_realation.xlsx'
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer, index=True, encoding='utf-8', sheet_name='pos_ngrams')
    writer.save()
    print("Successfully Saved!")
    end = time.time()
    print("------> It costs %ss" % end)

