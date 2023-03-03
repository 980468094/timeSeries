import pandas as pd


def readData(fileName):
    """
    读取数据
    :param fileName:
    :return:
    """
    df = pd.read_table(fileName)

    df = df[df['pwrBox180'] == 1]
    df = df[df['pwrBox97'] != 0]
    df = df.drop(
        ['milliseconds', 'pwrBox34_pwr', 'pwrBox99100', 'pwrBox101102',
         'pwrBox107', 'pwrBox108',
         'pwrBox111112', 'pwrBox113114', 'pwrBox115116',
         'pwrBox127130', 'pwrBox141144', 'pwrBox145',
         'pwrBox146', 'pwrBox147', 'pwrBox148', 'pwrBox149',
         'pwrBox150', 'pwrBox151', 'pwrBox152', 'pwrBox153',
         'pwrBox154', 'pwrBox155156', 'pwrBox157158', 'pwrBox159160',
         'pwrBox161162', 'pwrBox163164', 'pwrBox165166', 'pwrBox167168',
         'pwrBox169170', 'pwrBox171172', 'pwrBox173', 'pwrBox174', 'pwrBox180'], axis=1)
    return df
