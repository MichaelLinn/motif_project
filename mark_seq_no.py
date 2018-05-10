# -*- coding: utf-8 -*-
# @Time    : 5/3/18 7:57 PM
# @Author  : Jason Lin
# @File    : mark_seq_no.py
# @Software: PyCharm

import pandas as pd
import numpy as np

file = "./data/motif_encode.csv"
data = pd.read_csv(file)


flag = data.ix[0]['encode_no']
print(flag)

seq = []
i = 1
for index, row in data.iterrows():
    encode_no = row['encode_no']
    if flag == encode_no:
        seq.append(i)
        i += 1
    else:
        flag = encode_no
        i = 1
        seq.append(i)
        i += 1

data['seq_no'] = seq

data.to_csv("motif_encode_seq.csv", index=False)