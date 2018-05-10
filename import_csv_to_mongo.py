# -*- coding: utf-8 -*-
# @Time    : 5/2/18 8:54 PM
# @Author  : Jason Lin
# @File    : import_csv_to_mongo.py
# @Software: PyCharm

import sys
import pandas as pd
import pymongo
import json
import os

def import_content(filepath):
    mng_client = pymongo.MongoClient('10.37.0.118', 27017)
    mng_db = mng_client['motif']
    collection_name = 'motifhyades_results'
    db_cm = mng_db[collection_name]
    cdir = os.path.dirname(__file__)

    file_res = os.path.join(cdir, filepath)
    print(file_res)

    data = pd.read_csv(file_res)
    data_json = json.loads(data.to_json(orient='records'))
    db_cm.remove()
    db_cm.insert(data_json)

if __name__ == "__main__":
  filepath = 'motifhyades_result.csv'
  import_content(filepath)