import time
import warnings


def de_references(txt):
    """to delete references for every document"""
    if txt:
        word_amount = len(txt)
        indexes = []
        for index in range(word_amount):
            if txt[index] + txt[index + 1:index + 4] == "参考文献" \
                    or txt[index] + txt[index + 1:index + 2] == "注释" and index + 3 < word_amount:
                indexes.append(index)
        if len(indexes) > 0:
            index2 = indexes[-1]
            txt = txt.replace(txt[index2:], "")
            return txt
        else:
            Warning("no pre_index found!")
            return txt
    else:
        return txt


def de_pre(txt):
    """to delete content before main body"""
    global index
    if txt:
        word_amount = len(txt)
        name_index = []

        for index in range(word_amount):
            if txt[index] + txt[index+1 : index + 5] == "文献标识码" and index + 5 < word_amount:
                name_index.append(index)

        if name_index:
            if len(name_index) > 0:
                body = txt.replace(txt[:name_index[0]+8], "")
                return body
            else:
                warnings.warn("no pre_index found!")
                return txt
        else:
            return txt
    else:
        return txt


def extract_abstract(filepath):
    """ to extract abstract in the document"""
    start = time.time()
    with open(filepath, 'rb') as fo:
        content = fo.read()
        txt = content.decode(encoding="utf-8", errors="surrogateescape")
        word_amount = len(txt)
        indexes = [index for index in range(int(word_amount/5)) if txt[index] + txt[index+2] == "摘要" and index+1 < int(word_amount/5)]
        if len(indexes)>0:
            abs_index = indexes[0]
        else:
            warnings.warn("no abs_index found!")
        end_index = [index for index in range(int((word_amount/5))) if txt[index] + txt[index+1:index+3] == "关键词" and index + 3 < int(word_amount/5)]
        abstract = txt[abs_index:end_index[0]]
        fo.close()
    end = time.time()
    times = end - start
    print("Done! It costs -----> %ss." % times)
    return abstract


def de_header(txt):

    return


def de_footer(txt):

    return pure

def extract_main_body(filepath):
    """to call de_pre and de_reference to extract main body \
    from txt files directly"""
    start = time.time()
    with open(filepath, 'rb') as f:
        content = f.read()
        txt = content.decode(encoding="utf-8", errors="surrogateescape")
        half = de_pre(txt)
        main_body = de_references(half)
        f.close()
    if len(main_body) < 2:
        print("s% need a reprocessing!" % filepath)
    else:
        end = time.time()
        times = end - start
        print("Successfully extracted! It costs --->> %ss." % times)
        return main_body


if __name__ == '__main__':
    main_body = extract_main_body(r"F:\9.txt")
    #abstract = extract_abstract(r"F:\9.txt")
    print(main_body)


