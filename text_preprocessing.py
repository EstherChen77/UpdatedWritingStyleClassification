import re
import numpy as np
import pandas as pd
import os, codecs
import glob
import shutil
import jieba
from collections import Counter
from jieba import analyse
import jieba.posseg as pseg

'''
def parse_file(target_path):
    """to read file from file paths"""
    with open(target_path, 'rb') as file:
        content = file.read()
        text = content.decode('utf-8')
        # to delete /n and /w
        file.close()
    return text
'''


def remove_elements(sentences, ele):
    txt = sentences
    text = re.sub(ele, '', txt)
    return text


def remove_non_chinese(sentence):
    """to remove non chinese character"""
    content = [sentence]
    chinese_list = []
    for line in content:
        chinese_list.append(format_str(line))
    return chinese_list[0]


def is_chinese(uchar):
    """汉字编码区间"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def format_str(content):
    """to recognize chinese character"""
    content_str = ""
    for i in content:
        if is_chinese(i):
            content_str = content_str + i
    return content_str


def remove_punc(sentences):
    punct = set(u''':!):;?]}¢'〉=>/」』】〕〗〞︰︱︳﹒］
    ﹔﹕﹖﹗﹚﹜﹞）．｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
    々‖•·ˇˉ―--′’([{£¥'‵〈「『【〔〖（［｛￡￥〝︵︷︹︻
    ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…''')
    # for str/unicode
    filter_punt = lambda s: ''.join(filter(lambda x: x not in punct, s))
    # for list
    filter_punt_l = lambda l: list(filter(lambda x: x not in punct, l))
    if isinstance(sentences, str):
        filter_text = filter_punt(sentences)
    else:
        filter_text = filter_punt_l(sentences)
    return filter_text


def get_words_pos_freq(sentences, length, n):
    """n means top n words in sentences"""
    c = Counter()
    words = pseg.cut(sentences)
    for (word, flag) in words:
        m = length - 1
        if len(word) > m:
            c[(word, flag)] += 1
    print('高频词汇及词性统计：')
    for (k, v) in c.most_common(n):
        print('%s%s %s  %d' % ('  ' * (5 - len(k)), k, '*' * int(v / 180), v))


def topic_word_anal(sentences, pos, topK):
    words_list = analyse.textrank(sentences, topK=topK, allowPOS=pos)
    print('语料中前%s个词性为%s的主题词为：%s' % (topK, pos, words_list))


if __name__ == '__main__':
    # to parse txt file
    path = r'E:/Ipython/Machine Learning/research/corpus_by_gene/'
    filename_list = [30,40,50,'60pre','60pos',70,80]
    for file_name in filename_list:
        content = parse_file(path+ str(file_name) + '.txt')
        corpus = content

        # to remove useless char
        useless_char = ['\n', '\t', ' ']
        pure_text = corpus
        for char in useless_char:
            pure_text = remove_elements(pure_text, char)

        # to remove non_chinese char
        text = remove_non_chinese(pure_text)

        print('%s%s' % (file_name, '年代：'))

        # to analyze word frequency
        get_words_pos_freq(text, 2, 50)

        # to extract topic words by pos
        topic_word_anal(text, 'v', 20)

        topic_word_anal(text, 'adv', 20)