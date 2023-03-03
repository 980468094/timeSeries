import os
import matplotlib.pyplot as plt

from base import readData


class DataProcess():
    """
    数据预处理
    """

    def __init__(self, fileName):
        self.df = readData(fileName)

    def pwrBox97(self, filName, feature):
        """
        查看机组工作状态分步
        :param filName:   df数据
        :param feature:   要查看的特征名
        :return:
        """
        df = filName.drop(['pwrBox118', 'pwrBox119', 'pwrBox120', 'pwrBox121', 'pwrBox122', 'pwrBox123', 'pwrBox124',
                           'pwrBox125', 'pwrBox126'], axis=1)

        plt.figure(figsize=(15, 10))
        plt.plot(df[feature], marker='o')
        plt.grid()  # 添加网格线
        plt.show()

    def chooseNormalData(self, filName):
        """
        筛选pwrBox97为9的数据（正常运行数据）
        :return:
        """
        # self.df = self.df[self.df['pwrBox97'] == 9]
        return self.df

    def generateLabel(self):
        """
        生成数据标签
        :return:
        """
        # 如果电压不在374~386之间标签为True， 在的话标签为False
        self.df['label'] = self.df['pwrBox6768'].between(374, 386)
        self.df['label'] = self.df['pwrBox6970'].between(374, 386)
        self.df['label'] = self.df['pwrBox7172'].between(374, 386)
        print(self.df['label'])
        return self.df

    def splitDataByDay(self, perFile, data1):
        """
        根据天切分数据
        :param data:
        :return:
        """
        data1[['day', 'time']] = data1['datetime'].str.split(pat='T',expand=True)[[0,1]]
        day = df.groupby('day').count().index   # 获取当前数据中所有的日期
        for perDay in day:
            print(perDay)
            perDayData = df[df['day'] == perDay]
            perDayData.drop('datetime', axis=1)
            perDayData.to_csv('../testData/{}/{}.csv'.format(perFile, perDay))


    def delProData(self, perFile):

        rootPath = "../testData/{}".format(perFile)
        dataList = os.listdir(rootPath)
        if len(dataList) > 0:
            for i in dataList:
                os.remove(rootPath+'/{}'.format(i))


if __name__ == '__main__':

    pathDir = os.listdir("../data")
    for perFile in pathDir:
        filname = '../data/{}'.format(perFile)
        dataProcess = DataProcess(filname)
        df = dataProcess.chooseNormalData(filName=filname)
        print(filname)
        dataProcess.delProData(filname.split('tbl_')[1][:-4])
        dataProcess.splitDataByDay(filname.split('tbl_')[1][:-4], df)