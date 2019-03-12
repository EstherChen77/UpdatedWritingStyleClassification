
"""
    index_list = []
    for i in range(5):
        amount = len(sentences)
        batch = int(amount/4)
        index = batch + batch*(i-1)
        index_list.append(index)
    indexes = []
    for i in range(len(index_list)):
        if i+1 < len(index_list):
            index = (index_list[i], index_list[i+1])
            indexes.append(index)
    print(indexes)
    sen_index = []
    for i in range(4):
        for j in range(indexes[i][0], indexes[i][1], 1):
            sen_index.append(j)
    print(sen_index)
    sen_args = [sentences[indexes[i][0]:indexes[i][1]] for i in range(4)]
"""
    # multiprocessing.freeze_support()  # Windows，避免 RuntimeError

    # 8进程会直接崩溃电脑宕机, 多进程调用sql会锁死
    #pool = ProcessPool(nodes=4)
    #for i in range(len(sen_args)):
        #pool.map(dependency_analysis, sen_args, sen_index)

    #pool.close()
    #pool.join()