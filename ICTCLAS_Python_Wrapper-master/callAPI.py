from nlpir import *  # 导入nlpir.py文件

# 设置词性标注集
SetPOSmap(2)

def parse_file(target_path):
    """to read file from file paths"""
    with open(target_path, 'rb') as file:
        content = file.read()
        text = content.decode('utf-8')
        # to delete /n and /w
        file.close()
    return text

# 调用nlpir.py中的Seg（）函数，对字符串分词
p = '国家主席习近平4月11日到湖北省武汉市考察工作。'
p = p.encode('UTF8')
s = ''
for t in Seg(p):
    s += '%s/%s' % (t[0], t[1])
print(s)

path = r'E:/Ipython/Machine Learning/research/corpus_by_gene/30.txt'
content = parse_file(path)
text = content.encode('UTF8')
s = ''
for t in Seg(text):
    s += '%s/%s' % (t[0], t[1])
print(s)
