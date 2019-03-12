from Integrate import *

class LBTrie:
    """
    simple implemention of Trie in Python by authon liubing, which is not
    perfect but just to illustrate the basis and principle of Trie.
    """

    def __init__(self):
        self.trie = {}
        self.size = 0

    # 添加单词
    def add(self, word):
        p = self.trie
        word = word.strip()
        for c in word:
            if not c in p:
                p[c] = {}
            p = p[c]
        if word != '':
            # 在单词末尾处添加键值''作为标记，即只要某个字符的字典中含有''键即为单词结尾
            p[''] = ''

            # 查询单词

    def search(self, word):
        p = self.trie
        word = word.lstrip()
        for c in word:
            if not c in p:
                return False
            p = p[c]
        # 判断单词结束标记''
        if '' in p:
            return True
        return False


def match_academic(cuts):
    file = open("F:/paperdownload/G25.txt",encoding='utf-8')
    amount = 0
    for voca in file.readlines():
        trie_obj = LBTrie()
        trie_obj.add(voca)
        for word in cuts:
            if trie_obj.search(word)== 1:
                amount += 1
    return amount


if __name__ == '__main__':
    start = time.time()
    content = parse_file('F:/30.txt')
    sentences = content.split('。')
    alist = []
    cut_word = []
    for sen in sentences:
        pack = seg_sen(sen)
        cut_words = pack[1]
        pos_list = pack[0]
        cut_word.append(len(cut_words))
        amount = match_academic(cut_words)
        alist.append(amount)
    end = time.time()
    print('%s words takes %s seconds. %s seconds for each word.'%(sum(cut_word),(end-start),((end-start)/sum(cut_word))))