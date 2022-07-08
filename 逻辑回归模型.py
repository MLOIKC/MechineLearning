import numpy as np
import matplotlib.pyplot as plt
 
 
# 加载数据
def loadData(filename):
    """
    :param filename: 文件路径名
    :return:
    """
    # 读取数据
    fr = open(filename)
    # 原始数据集
    dataMat = []
    # 标签数据集
    lableMat = []
    # readlines() 方法用于读取所有行(直到结束符 EOF)并返回列表
    for line in fr.readlines():
        # strip()表示删除掉数据中的换行符，split()则是数据中遇到空格就隔开。
        lineArr = line.strip().split()  # 读取每一行数据
        # dataMat.append(lineArr)  # 将每一行数据添加到dataMat中
        # 为了方便计算，我们将 X0 的值设为 1.0 ，也就是在每一行的开头添加一个 1.0 作为 X0
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        lableMat.append(float(lineArr[2]))  # 将每一行的标签添加到lableMat中
 
    return dataMat,lableMat
 
 
# 定义sigmoid函数(相当于一个分类函数)
def sigmoid(x):
    """
    :param x: 函数变量
    :return: 返回函数值z
    """
    z = 1 / (1 + np.exp(-x))
    return z
 
 
 
# 梯度上升
def gradAscent(dataMat,classLables):
    """
    :param dataMat: 数据集
    :param classLables: 标签集
    """
    # 将数组转化为矩阵
    dataMarix = np.mat(dataMat)  # (100,3)
    # 将行向量转为列向量
    lableMat = np.mat(classLables).transpose()
    # m = 100 , n = 3
    m,n = np.shape(dataMarix)
    # 设置目标移动的步长(换个角度理解也就是设置学习率)
    lr = 0.001
    # 设置迭代次数
    epoch = 500
    # 设置初始的参数，并都赋默认值为1(生成一个长度和特征数相同的矩阵，此处n为3 -> [[1],[1],[1]])
    w = np.ones((n,1))
    for k in range(epoch):
        h = sigmoid(dataMarix * w)  # dataMarix * w : (100,3) * (3,1) = (100,1)
        # 真实值与预测值之间的差值
        loss = lableMat - h
        # 迭代更新回归系数w
        w +=  lr * dataMarix.transpose() * loss  # w : (3,1)
 
    return w
 
 
# 展示结果
def show(data,lable,w):
    """
    :param data: 数据集
    :param lable: 标签集
    :param w: 回归系数
    """
    # 获取样本总数
    n = len(data)
    # 定义列表用来存储每个点的横纵坐标
    x1 = []
    y1 = []
    x2 = []
    y2 = []
 
    # 迭代将同一类别的标签归为一类(0和1)
    for i in range(n):
        if lable[i] == 1 :
            x1.append(data[i,1])
            y1.append(data[i,2])
        else:
            x2.append(data[i,1])
            y2.append(data[i,2])
 
    # 绘图
    plt.scatter(x1, y1, s=30, c='blue', marker='s')
    plt.scatter(x2, y2, s=30, c='green')
    # 画拟合曲线
    x = np.arange(0,15,0.1)  # 这里主要是根据我们的数据集来自定义横轴刻度
    y = -(w[0] + w[1] * x) / w[2]  # y变量主要根据 z =  w0x0 + w1x1 + w2x2 推导出来的
    plt.plot(x,y)
    plt.show()
 
 
 
 
if __name__ == '__main__':
    data,lable = loadData('D:\作业\机器学习实践\逻辑回归算法\\wine.txt')
    w = gradAscent(data,lable)
    show(np.mat(data),lable,w)
