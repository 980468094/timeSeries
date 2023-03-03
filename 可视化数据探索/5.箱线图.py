import numpy as np

from base import readData
import matplotlib.pyplot as plt

fileName = '../data/Y4_2022-07-01_tbl_pwrarrypwrcar1.csv'
df = readData(fileName)
print(df.columns)
df = df[['pwrBox6768', 'pwrBox6970', 'pwrBox7172', 'pwrBox7374',
       'pwrBox7576', 'pwrBox7778', 'pwrBox7980', 'pwrBox8182', 'pwrBox8384',
       'pwrBox8586', 'pwrBox87']]
labels = 'pwrBox6768', 'pwrBox6970', 'pwrBox7172'
plt.grid(True)  # 显示网格
plt.boxplot([df['pwrBox6768'], df['pwrBox6970'],df['pwrBox7172']],
            medianprops={'color': 'red', 'linewidth': '1.5'},
            meanline=True,
            showmeans=True,
            meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1.5'},
            flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 10},
            labels=labels)
plt.show()


labels = 'pwrBox7374','pwrBox7576', 'pwrBox7778'
plt.grid(True)  # 显示网格
plt.boxplot([df['pwrBox7374'], df['pwrBox7576'],df['pwrBox7778']],
            medianprops={'color': 'red', 'linewidth': '1.5'},
            meanline=True,
            showmeans=True,
            meanprops={'color': 'blue', 'ls': '--', 'linewidth': '1.5'},
            flierprops={"marker": "o", "markerfacecolor": "red", "markersize": 10},
            labels=labels)
plt.show()