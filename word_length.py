from preprocessing import parse_file
import numpy as np
import pandas as pd
import os


def get_sen_mean(sen):
    if len(sen) > 0:
        avg = sum([int(i) for i in sen if i])/len(sen)
        return avg
    else:
        pass

def frequ(sen, num):
    inifreq = 0
    for word in sen:
        if int(word) == num:
            inifreq += 1
    return inifreq


def frequ_matrix(sentences, num):
    fmatrix = [frequ(sen, num) for sen in sentences]
    return fmatrix


def get_var(avgs):
    var = np.var([avg for avg in avgs if avg], ddof=1)
    return var

if __name__ == '__main__':
    # to get statistics by person
    # to get files
    path = 'F:/down' + '/'
    name_list = os.listdir(path)
    dic_list = []
    for name in name_list:
        file_path = 'F:/final/' + name + '/' + 'word_length.txt'
        content = parse_file(file_path)
        sentences = content.split(".")
        # to calculate average word_length
        avgs_sen = [get_sen_mean(sen) for sen in sentences]
        avg_sens = get_sen_mean(avgs_sen)
        # to calculate variance in a document
        var = get_var(avgs_sen)
        # to cal n-words frequency
        freq = []
        for i in range(1, 6):
            freq.append(get_sen_mean(frequ_matrix(sentences, i)))
        dict = {"name": name, "avg_wo_len": avg_sens, "var" : var, "1-word": freq[0],
                "2-word": freq[1],"3-word": freq[2],"4-word": freq[3],"5-word": freq[4]}
        dic_list.append(dict)

    df = pd.DataFrame(dic_list)
    # to save as .xlsx
    file_path = r'E:/Ipython/Machine Learning/research/data/by_author/word_length.xlsx'
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer, index=True, encoding='utf-8', sheet_name='pos_ngrams')
    writer.save()
    print("Successfully Saved!")






