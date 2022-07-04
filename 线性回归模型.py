import numpy as np
from mpl_tooolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt

#读取数据集
def loaddata(filename):
    dataset=[]
    fp=open(filename)
    for i in fp.readlines():
        #如果数据过于庞大，只是用前1000个数据
        if len(dataset)>=1000:
            break
        a=i.strip().split()

        dataset.append([float(a[3]),float(a[4]),float(a[5])])
        #将数据集的第3，4，5列的数据，形成一个三维的dataset
    return dataset

#可视化数据，进行绘制回归曲线
def Data_plot(data,w):
    x=data[:,0]
    y=data[:.1]
    z=data[:,2]

    x1=[0,600]
    
