import pandas as pd
from base import readData
import matplotlib.pyplot as plt

filname = '../testData/pwrcar1.csv'
df = readData(fileName=filname)
# df = df.drop(['datetime', 'pwrBox180', 'pwrBox175', 'pwrBox117', 'pwrBox118',
#                   'pwrBox119', 'pwrBox120', 'pwrBox121', 'pwrBox122', 'pwrBox123',
#                   'pwrBox124', 'pwrBox125', 'pwrBox126'], axis=1)

plt.figure(figsize=(20, 10))
plt.plot(df[['pwrBox87','pwrBox88']], 'o-r')
plt.plot(df[['pwrBox88']], 'o-g')
plt.grid()
plt.show()
