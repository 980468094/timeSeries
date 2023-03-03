# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author : Lawrence
# @File : 2.建模.py
# @Project : 23power
# @Time : 2023/3/3 10:41

# -*- coding: UTF-8 -*-

# 导入所需模块
import os

import pandas as pd
import tensorflow as tf
import numpy as np

# 导入数据，分别为输入特征和标签
# x_data = datasets.load_iris().data
# y_data = datasets.load_iris().target
# print(x_data)


def loadData(filePath):
    x_data = pd.DataFrame()
    for perData in filePath:
        x_data = perData


filePath = '../testData/pwrarrypwrcar1'
listDir = os.listdir(filePath)
xData = pd.DataFrame()
yData = pd.DataFrame()
xLabel = ['pwrBox6768', 'pwrBox6970', 'pwrBox7172', 'pwrBox7374', 'pwrBox7576',
                           'pwrBox7778', 'pwrBox7980', 'pwrBox8182', 'pwrBox8384', 'pwrBox8586',
                           'pwrBox87', 'pwrBox88', 'pwrBox8990', 'pwrBox9192', 'pwrBox9394',
                           'pwrBox9596', 'pwrBox97', 'pwrBox98', 'pwrBox109', 'pwrBox110',
                           'pwrBox131132', 'pwrBox133134', 'pwrBox135136', 'pwrBox175']
yLabel = ['pwrBox117']
for perData in listDir:
    tmpData = pd.read_csv(filePath + '/' + perData)
    tmpData['pwrBox117'] = tmpData['pwrBox117'].replace(255, 1)
    xData = pd.concat([xData, tmpData[xLabel]], axis=0)  # 合并x列的值
    yData = pd.concat([yData, tmpData[yLabel]], axis=0)  # 合并y列的值

# print(xData)
# print(yData)

x_train, y_train = xData.values, yData.values.reshape(-1)
# x_train, y_train = xData.values, yData.values
print(x_train.shape)
print(y_train.reshape(-1))

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(2, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2())
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
              metrics=['sparse_categorical_accuracy'])

model.fit(x_train, y_train, batch_size=32, epochs=50, validation_split=0.2, validation_freq=20)

model.summary()