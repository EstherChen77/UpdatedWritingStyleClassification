from dependency_count import *
from word_length import *
from nlpir import *
import matplotlib.pyplot as plt
import numpy as np

SetPOSmap(2)
f = open("F:/paperdownload/G25.txt",'r',encoding='utf-8',errors="surrogateescape")
for word in f.readlines():
    AddUserWord(word.encode('UTF8')+b'\t'+b'n')


def match_academic(cuts):
    file = open("F:/paperdownload/G25.txt",encoding='utf-8')
    amount = 0
    for voca in file.readlines():
        for word in cuts:
            if str(voca[:-1]) == str(word):
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
    f = open("F:/paperdownload/G25.txt", 'r', encoding='utf-8', errors="surrogateescape")
    for word in f.readlines():
        AddUserWord(word.encode('UTF8') + b'\t' + b'n')
    for t in Seg(p):
        pos_list.append(t[1])
        words_list.append(t[0])
    return [pos_list, words_list]


class Pos(object):
    def __init__(self, pos_list):
        self.x = pos_list
        self.y = len(pos_list)
        self.candidate = [['v', 'vg', 'vd'], ['n', 'nr', 'ns', 'nt', 'nz', 'vn'], ['Ag', 'a', 'ad', 'an'], ['e', 'y', 'o'],
        ['d', 'g','Dg'],['c']]

    def count(self, option=6):
        target = self.candidate[option]
        amount = 0
        for p in target:
            for v in self.x:
                if v == p:
                    amount += 1
        return (amount)


    def cal_all(self):
        all = []
        for i in range(6):
            all.append(self.count(i))
        return all


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
    for gene in range(1,8):#1,8
        path = 'F:/final/'+str(gene) +'/'
        for name in os.listdir(path):
            file_path = path + name + "/"
            files = len(os.listdir(file_path))
            for file_name in range(files-2): #files-2
                print("-" * 30 + "->for %s, this is %s in %s papers" % (name, file_name, files - 3))
                dire = file_path + str(file_name) + ".txt"
                content = parse_file(dire)
                sentences = content.split("。")
                if len(sentences)>=10:
                    for i in range(len(sentences)):
                        SetPOSmap(2)
                        f = open("F:/paperdownload/G25.txt", 'r', encoding='utf-8', errors="surrogateescape")
                        for word in f.readlines():
                            AddUserWord(word.encode('UTF8') + b'\t' + b'n')
                        dic = by_sentence(sen=sentences[i],gene=gene,sen_index=i,name = name, paper_index=file_name,sen_count = len(sentences))
                        if dic:
                            dictList.append(dic)
                else:
                    pass

    df = pd.DataFrame(dictList)
    # to save as .xlsx
    file_path = r'E:/Ipython/Machine Learning/research/data/again2.xlsx'
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer, index=True, encoding='utf-8', sheet_name='pos_ngrams')
    writer.save()
    print("Successfully Saved!")
    end = time.time()
    print("------> It costs %ss" % end)

