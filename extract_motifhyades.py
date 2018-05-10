# -*- coding: utf-8 -*-
# @Time    : 5/1/18 3:11 PM
# @Author  : Jason Lin
# @File    : extract_motifhyades.py
# @Software: PyCharm

from pymongo import MongoClient
import pprint
from collections import OrderedDict
import re

client = MongoClient('10.37.0.118', 27017)
db = client.motif
motif_h = db.motifhyades_middle_res
encode_data = db.input_data

# cur = encode_data.find({},{'encode_no':1, "_id":0}).distinct('encode_no')
# total_encode = len(cur)

def get_motifhyades():

    for post in motif_h.find(no_cursor_timeout=True).batch_size(5):
        # print(post)
        encode_no = int(post['encode_no'])

        first_motifs = post['content']['first_motif']
        first_width = post['first_width']
        second_motifs = post['content']['second_motif']
        second_width = post['second_width']
        # first motif: enhancer
        # second motif: promoter (upstream and downstream)
        for i in range(len(first_motifs)):
            print("-------------", i ,"-------------")
            seq_keys = list(first_motifs.keys())
            seq = seq_keys[i]

            first_pos = int(first_motifs[seq])
            second_pos = int(second_motifs[seq])

            seq_no = int(seq.split('q')[1])
            if seq_no % 2 == 1:
                flag = "up"
                seq_no += 1
            else:
                flag = "down"
            seq_no /= 2
            encode_info = get_encode_info(encode_no, seq_no)
            promoter_pos, enhancer_pos = cal_absolute_motif_pos(flag, first_pos, first_width, second_pos, second_width, encode_info)


            with open("motifhyades_result.csv", "a") as f:
                f.write(str(encode_no) + "," + encode_info['chr_type'] + "," + enhancer_pos + "," + str(first_width)
                        + "," + promoter_pos + "," + str(second_width) + '\n')
            print(promoter_pos, enhancer_pos)


def cal_absolute_motif_pos(flag, first_pos, first_width, second_pos, second_width, encode_info):
    # first motif -> enhancer
    # second motif -> promoter

    enhancer = encode_info['enhancer']
    chr_type = encode_info['chr_type']
    if flag == "up":
        promoter = encode_info['promoter_up']
    else:
        promoter = encode_info['promoter_down']

    enhancer_start = re.split(":|-", enhancer)[1]
    enhancer_start = int(enhancer_start) + first_pos
    enhancer_end = enhancer_start + int(first_width)

    promoter_start = re.split(":|-", promoter)[1]
    promoter_start = int(promoter_start) + second_pos
    promoter_end = promoter_start + int(second_width)

    promoter_pos = chr_type + ":" + str(promoter_start) + '-' + str(promoter_end)
    enhancer_pos = chr_type + ":" + str(enhancer_start) + '-' + str(enhancer_end)

    return promoter_pos, enhancer_pos


def get_encode_info(encode_no, seq_no):
    # odd seq is up promoter, even is down promoter
    encode_info = encode_data.find_one({'encode_no': encode_no, "seq_no": seq_no})
    # print(encode_info)
    return encode_info


with open("motifhyades_result.csv", "a") as f:
    f.write("encode_no,chr_type,enhancer,enhancer_width,promoter,promoter_width\n")
get_motifhyades()






