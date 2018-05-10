# -*- coding: utf-8 -*-
# @Time    : 4/24/18 11:23 AM
# @Author  : Jason Lin
# @File    : build_motifhyades_mongo.py
# @Software: PyCharm

#  generate the MotifHyades_res MONGODB

import numpy as np
import os
import re
from pymongo import MongoClient
from collections import OrderedDict


# Motif info from MotifHyades

def getMHMotif():
    foldname = "../MotifHyades_results/"
    os.getcwd()
    fold_list = os.listdir(foldname)
    encode_l = []
    for fold in fold_list:
        if fold.split("_")[2] == "encode" and fold.split(".")[-1] != ".mat":
            encode_l.append(fold)

    print("ENCODE_file number:", len(encode_l))
    # print(encode_l)
    test = {}

    for res in encode_l:
        subfold = foldname + res
        t = res

        encode_no = t.split("_")[3]
        # test[encode_no] = test.get(encode_no, 0) + 1
        res = os.listdir(subfold)
        # print(res)
        for pair in res:
            filename = subfold + "/" + pair
            # record the params (p_w, e_w, motif_no)  of motif
            motif_no = pair.split("_")[3]
            # print(pair)
            pair_no = re.split(r"_|\.", pair)[-2]
            p_w = pair.split("_")[10].split("p")[1]
            e_w = pair.split("_")[11].split("e")[1]
            # print(motif_no,pair_no, p_w, e_w)
            motif_1, motif_2 = extract_info_from_hyades(filename)
            post = [motif_no, pair_no, p_w, e_w, motif_1, motif_2]
            # print(post)
            insert_mongodb(post)


def insert_mongodb(info_list):
    post = {}
    post["encode_no"] = info_list[0]
    post["pair_no"] = info_list[1]
    post["first_width"] = info_list[2]
    post["second_width"] = info_list[3]

    motif_1 = info_list[4]

    motif_2 = info_list[5]
    first_motif = OrderedDict()
    second_motif = OrderedDict()
    content = {}

    for i in range(len(motif_1)):
        first_motif[motif_1[i][0]] = motif_1[i][1]
    # print(first_motif)
    for i in range(len(motif_2)):
        second_motif[motif_2[i][0]] = motif_2[i][1]

    content["first_motif"] = first_motif
    content["second_motif"] = second_motif

    post["content"] = content
    # print(content)
    print(post)

    client = MongoClient('10.37.0.118', 27017)
    db = client.motif

    collection = db.motifhyades_res
    collection.insert_one(post)


def extract_info_from_hyades(filename):
    # print(filename)
    with open(filename, "r") as motif_f:
        motif_1 = []
        motif_2 = []
        flag = 0
        pattern1 = re.compile(r'first motif locations')
        pattern2 = re.compile(r'second motif locations')
        EOF = re.compile("END")
        while True:
            line = motif_f.readline()
            if EOF.search(line):
                break

            if pattern1.search(line):
                flag += 1
                continue
            if pattern2.search(line):
                flag += 1
                continue
            if flag == 1:
                t = line.split(',')
                motif_1.append([t[0], t[1]])
            if flag == 2:
                t = line.split(',')
                motif_2.append([t[0], t[1]])
            if not line:
                break

    motif_1.sort(key = lambda motif_1: int(motif_1[0].split('q')[1]))
    motif_2.sort(key = lambda motif_2: int(motif_2[0].split('q')[1]))

    return motif_1, motif_2

getMHMotif()