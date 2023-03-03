from base import readData
import pandas as pd
#
# fileName = r'E:\Users\18640\Desktop\工作内容\2院\雷达冷却系统\新设备数据\冷却车.xlsx'
#
# df = pd.read_excel(fileName)
# # df = df.drop(['Unnamed: 0'], axis=1)
# df.to_csv('./冷却车.csv')
# print(df.head())

import pandas as pd

# df = pd.read_csv('./testData/pwrpwrfreqcar2.csv')
# df[['day', 'time']] = df['datetime'].str.split(pat='T',expand=True)[[0,1]]
# # print(df[['day', 'time']])
# day = df.groupby('day').count().index
# for i in day:
#     perDayData = df[df['day'] == i]
#     print(perDayData)
#     break

df = pd.read_table('./data/Y4_2022-07-01_tbl_pwrarrypwrcar3.txt')
print(df['pwrBox117'].value_counts())
