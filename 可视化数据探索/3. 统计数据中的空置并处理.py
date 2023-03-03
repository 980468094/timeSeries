# load dataset
from numpy import isnan
from numpy import count_nonzero
from pandas import read_csv
import numpy

from base import readData

filname = './data/Y4_2022-07-01_tbl_pwrarrypwrcar1.csv'
df = readData(fileName=filname)

print(df.shape)
# 转为浮点数
values = df.values
data = values[:, :].astype('float32')
# 统计缺失值
total_missing = count_nonzero(isnan(data))
percent_missing = total_missing / data.size * 100
print('总的缺失值为: %d/%d (%.1f%%)' % (total_missing, data.size, percent_missing))