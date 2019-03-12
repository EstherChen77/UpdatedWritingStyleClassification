import os
import pandas as pd

"""to count files in every path"""
'''
path = 'F:/down' + '/'
name_list = os.listdir(path)
file_nums = []
for name in name_list:
    file_path = 'F:/down' + '/' + name + '/'
    file_counts = len([name for name in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, name))])
    file_nums.append(file_counts)
df = pd.DataFrame(columns=("name", "counts"))
df['name'] = name_list
df["counts"] = file_nums

print(df)
'''


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def contains(string, word):
    if word in string:
        return True


def merge_txt(file_path, save_path, file_name):
    files = os.listdir(file_path)
    txts = [file for file in files if contains(file, file_name) == 1]
    print(txts)
    print('%s txt files got!'% len(txts))
    all_corpus = []
    for txt in txts:
        if os.path.exists(file_path+txt):
            with open(file_path+txt, 'rb') as f:
                content = f.read()
                txt = content.decode('UTF-8', errors="surrogateescape")
                all_corpus.append(txt)
                f.close()
    if os.path.exists(save_path) == 0:
        try:
            #os.remove(save_path)
            with open(save_path, 'w', encoding='utf-8') as new:
                new.write(str(all_corpus))
                new.close()
        except:
            FileExistsError("not a directory")
    print("Txt files merged!")




if __name__ == '__main__':
    path = 'F:/down' + '/'
    name_list = os.listdir(path)
    gene = [30, 40, 50, '60pre', '60pos', 70, 80]
    dict = []
    for ge in gene:
        name_path = 'F:/new/' + str(ge) + '/'
        gene_name_list = os.listdir(name_path)
        for name in name_list:
            for gene_name in gene_name_list:
                if name == gene_name:
                    dic = (name, ge)
                    dict.append(dic)
    print(dict)
    for i in range(len(name_list)):
        value = [dict[j][1] for j in range(len(dict)) if name_list[i] == dict[j][0]]
        print(value[0])


'''
    file_path = 'F:/word_length_bygene/'
    gene = [30, 40, 50, '60pre', '60pos', 70, 80]
    for ge in gene:
        file_name = str(ge)
        save_path = file_path + str(ge) + '.txt'
        merge_txt(file_path, save_path, file_name)
'''

'''
    gene = [30, 40, 50, '60pre', '60pos', 70, 80]
    for ge in gene:
        name_path =  'F:/new/' + str(ge) + '/'
        name_list = os.listdir(name_path)
        for name in name_list:
            file_path = 'F:/final/' + name + '/'
            save_path = 'F:/' + 'word_length_bygene' + str(str(ge) + '_' + name + 'word_length') + '.txt'
            file_name = 'word_length'
            merge_txt(file_path, save_path, file_name)
'''
#for i in range(len(name_list)):
#merge_txt("白国应")

