import re
import os


def parse_file(target_path):
    """to read file from file paths"""
    if os.path.exists(target_path) == 1:
        with open(target_path, 'rb') as file:
            content = file.read()
            text = content.decode('utf-8', errors="surrogateescape")
            # to delete /n and /w
            file.close()
        return text
    else:
        text = 'path error'
        return text


def remove_elements(sentences, ele):
    txt = sentences
    text = re.sub(ele, '', txt)
    return text


def remove_punc(sentences):
    if sentences:
        punct = set(u''':!).:;?]}¢'"〉=>/」』】〕〗〞︰︱︳､﹒］
        ﹔﹕﹖﹗﹚﹜﹞）．｜｝︴︶︸︺︼︾﹀﹂﹄﹏､～￠
        々‖•·ˇˉ―--′’”([{£¥'‵〈「『【〔〖（［｛￡￥〝︵︷︹︻
        ︽︿﹁﹃﹙﹛﹝（｛“‘-—_…
        ''')
        # for str/unicode
        filter_punt = lambda s: ''.join(filter(lambda x: x not in punct, s))
        # for list
        filter_punt_l = lambda l: list(filter(lambda x: x not in punct, l))
        if not isinstance(sentences, list):
            filter_text = filter_punt(sentences)
        else:
            filter_text = filter_punt_l(sentences)
        pure_text = re.sub(u'\u3000', u'', filter_text)
        return pure_text
    else:
        return sentences


def remove_useless_char(sentences):
    if sentences:
        pure_text = sentences
        useless_char = ['\n', '\t', ' ', '\r', " "]
        for char in useless_char:
            pure_text = remove_elements(pure_text, char)
        text = re.sub(u'\u3000', u'', pure_text)
        return text
    else:
        return sentences



if __name__ == '__main__':
    path = 'F:/down' + '/'
    name_list = os.listdir(path)
    for name in name_list[15:]:
        num = int((len(os.listdir(path + str(name))) - 1) / 2)
        print(num)
        for i in range(num):
            txt = parse_file(path + str(name) + '/' + str(i) + '.txt')
            if txt == "path error":
                pass
            else:
                # txt cleaning
                if txt:
                    text = remove_useless_char(txt)
                    text = de_annotation(text)
                    text = remove_punc(text)
                    new_str = de_useless_info(text, "作者简介")
                    str2 = de_useless_info(new_str, "收稿日期")

                    out = de_volume_form(str2)
                    no_put = de_pre(out)
                    keywords = 'Keywords'
                    if keywords in no_put:
                        no_put = de_pre_keyword(keywords, no_put)
                    keyword = 'Ｋｅｙｗｏｒｄｓ'
                    if keyword in no_put:
                        no_put = de_pre_keyword(keyword, no_put)
                    output = de_references(no_put)
                    output2 = de_references(output)
                    if output2:
                        print("%s, Txt file cleaned" % name)
                        name_path = 'F:/final' + '/' + str(name)
                        if os.path.exists(name_path) == 0:
                            os.makedirs(name_path)
                        write_path = name_path + '/' + str(i) + '.txt'
                        if os.path.exists(write_path) == 0:
                            with open(write_path, 'wb') as f:
                                f.write(output2.encode('utf-8', errors="surrogateescape"))
                                f.close()
                    else:
                        print("No text!")
                else:
                    pass