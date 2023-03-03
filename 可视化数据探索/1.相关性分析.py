import matplotlib.pyplot as plt
import seaborn as sns
from base import readData

filname = '../data/Y4_2022-07-01_tbl_pwrarrypwrcar1.csv'
df = readData(fileName=filname)
print(df.columns)
df = df.drop(['datetime', 'pwrBox180', 'pwrBox175', 'pwrBox117', 'pwrBox118',
                  'pwrBox119', 'pwrBox120', 'pwrBox121', 'pwrBox122', 'pwrBox123',
                  'pwrBox124', 'pwrBox125', 'pwrBox126'], axis=1)
corr = df.corr()
print(corr)

plt.figure(figsize=(20, 20))
sns.heatmap(corr, cmap='mako')
plt.show()
