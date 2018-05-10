# -*- coding: utf-8 -*-
# @Time    : 4/23/18 10:19 PM
# @Author  : Jason Lin
# @File    : Motif.py
# @Software: PyCharm


class Motif:
    chr_type = ""
    m_start = 0
    m_end = 0

    def __init__(self, chr_type):
        self.chr_type = chr_type

    def setChr_type(self, chr_t):
        self.chr_type = chr_t

    def setM_start(self, start):
        self.m_start = start

    def setM_end(self, end):
        self.m_end = end

class Motif_hyades:
    motif_p1 = 0
    motif_p2 = 0
    p_w = 0
    e_w = 0
    chr_type = ""
    motif_no = 0

    def __init__(self, chr_type, motif_p1, motif_p2, w_1, w_2, motif_no):
        self.chr_type = chr_type
        self.motif_p1 = motif_p1
        self.motif_p2 = motif_p2
        self.w_1 = w_1
        self.w_2 = w_2
        self.motif_no = motif_no















