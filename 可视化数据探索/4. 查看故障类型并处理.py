from matplotlib import pyplot
from numpy import unique

from base import readData


def viewMalfunctionType(filname):
    df = readData(fileName=filname)
    df = df[['pwrBox117', 'pwrBox118', 'pwrBox119', 'pwrBox120', 'pwrBox121', 'pwrBox122', 'pwrBox123',
             'pwrBox124', 'pwrBox125', 'pwrBox126']]

    features = ['pwrBox117', 'pwrBox118', 'pwrBox119', 'pwrBox120', 'pwrBox121', 'pwrBox122', 'pwrBox123',
                'pwrBox124', 'pwrBox125', 'pwrBox126']
    for feature in features:
        value_count = df[feature].value_counts()
        print('{}:'.format(feature))
        print(value_count)
        print('--------------------------------------')


# 通过'chunkID'列将数据分块
def to_chunks(values, chunk_ix=1):
    chunks = dict()
    # 去重，获取列中包含的序号
    chunk_ids = unique(values[:, chunk_ix])
    # 根据序号获取所有分组
    for chunk_id in chunk_ids:
        # 第一列满足条件的记为True，获取一个True/False列表
        selection = values[:, chunk_ix] == chunk_id
        # 返回标记为True的行
        chunks[chunk_id] = values[selection, :]
    return chunks



def plot_chunk_durations(chunks):
    # 统计每个数据块内的数据量，k,v是每个chunks.items()的键和值
    chunk_durations = [len(v) for k, v in chunks.items()]
    # boxplot
    pyplot.subplot(2, 1, 1)
    pyplot.boxplot(chunk_durations)
    # histogram
    pyplot.subplot(2, 1, 2)
    pyplot.hist(chunk_durations)
    # histogram
    pyplot.show()


if __name__ == '__main__':
    filname = '../data/Y4_2022-07-01_tbl_pwrpwrfreqcar2.csv'
    viewMalfunctionType(filname)
