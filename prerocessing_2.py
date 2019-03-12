import warnings
from preprocessing import *
from text_preprocessing import *
# only standard papers are considered to save time and energy

import re
def re_find(pattern, txt):
    """to simplifier re.match"""
    if txt:
        pa = re.compile(pattern)
        target_part = re.findall(pa, txt)
        return target_part
    else:
        return txt


def extract_pub_year(txt):
    """to extract publication year"""
    year_part = re_find(r"\d{4}年第\d{1}期", txt)
    if len(year_part) != 0:
        pub_year= year_part[0][:4]

    else:
        year_part = re_find(r"收稿日期：\d{4}", txt)
        pub_year = year_part[0][-4:]
    if len(pub_year) == 0:
        warnings.warn("No publication year found!")
    else:
        return pub_year




def de_annotation(text):
    """ to delete [d]"""
    if text:
        # to find singe[d]
        anno_single_list = re.findall(r"［\d{1,2}］", text)
        # to find double[d-d]
        anno_append_list = re.findall(r"\[\d{1,2}\]", text)
        anno_double_list = re.findall(r"［\d{1,2}－\d{1,2}］", text)
        # to find double[d,d]
        anno_triple_list = re.findall(r"［\d{1,2}，\d{1,2}］", text)
        anno_list = anno_single_list + anno_double_list + anno_triple_list + anno_append_list
        pure_text = text
        for anno in anno_list:
            pure_text = pure_text.replace(anno, "")
        return pure_text
    else:
        return text


def de_useless_info(text,target_four_word):
    """匹配想要删除的四个字所在句并delete"""
    if text:
        word_amount = len(text)
        indexes = [index for index in range(int(word_amount/5)) if
                   text[index] + text[index + 1:index + 4] == target_four_word
                 and index + 3 < word_amount]
        if len(indexes) > 0:
            tar_index = indexes[-1]
            period_index = [index for index in range(tar_index, word_amount,1) if
                   text[index] == "。"]
            try:
                txt = text.replace(text[tar_index:period_index[0]], "")
                return txt
            except IndexError:
                return text

        else:
            warnings.warn("no pre_index found!")
            return text
    else:
        return text


def de_volume_form(text):
    """to delete 第N卷，第N期"""
    global clear_text
    if text:
        volume_list_1 = re_find(r"第\d{1,3}期", text)
        volume_list_2 = re_find(r"第\d{1,3}卷", text)
        volume_list_3 = re_find(r"\(\d\)", text)
        volume_list = volume_list_1 + volume_list_2 + volume_list_3
        if volume_list:
            for volume in volume_list:
                clear_text = text.replace(volume, "")
                return clear_text
        else:
            return text
    else:
        return text




def de_pre_keyword(word, text):
    """匹配keyword并delete之前的string.In case there is no 文献标识码"""
    if text:
        pattern = re.compile(word)
        index_iter = re.finditer(pattern, text)
        if index_iter:
            for index in index_iter:
                end = index.end()
                post_keyword = text[end:]
                if post_keyword:
                    return post_keyword
                else:
                    return text
        else:
            return text

    else:
        return text


if __name__ == '__main__':
    file_path = r"F:\9.txt"
    with open(file_path, 'rb') as f:
        content = f.read()
        txt = content.decode(encoding="utf-8", errors="surrogateescape")
        text = remove_useless_char(txt)
        print(text)
        new_str = de_useless_info(text, "作者简介")
        str2 = de_useless_info(new_str, "收稿日期")
        final = de_annotation(str2)
        output = de_volume_form(final)
        f.close()
    with open(r'F:\multitest.txt','w',encoding="utf-8", errors="surrogateescape") as fo:
        fo.write(output)
        fo.close()




"""匹配乱码并delete, 无法解决"""

"""匹配页码并删除，无法解决"""

