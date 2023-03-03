# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : Lawrence
# @File : 抽取样本数据.py
# @Project : 23power
# @Time : 2022/11/11 10:09

import pandas as pd

pd.set_option('display.max_columns', None)
name = 'Y4_2022-07-01_tbl_pwrpwrfreqcar2.txt'
df = pd.read_table('./data/{}'.format(name))
print(df.columns)
df = df[['datetime','pwrBox6768','pwrBox6970','pwrBox7172','pwrBox7374','pwrBox7576','pwrBox7778',
'pwrBox7980','pwrBox8182','pwrBox8384','pwrBox8586','pwrBox87','pwrBox88','pwrBox9192','pwrBox9394',
'pwrBox9596','pwrBox97','pwrBox117','pwrBox118','pwrBox119','pwrBox120','pwrBox121','pwrBox122',
'pwrBox123','pwrBox124','pwrBox125','pwrBox126','pwrBox131132','pwrBox133134','pwrBox135136','pwrBox137140',
'pwrBox175','pwrBox180']]
df = df[df['pwrBox180']==1]
df.to_csv('./testData/{}.csv'.format(name.split('.')[0]))
