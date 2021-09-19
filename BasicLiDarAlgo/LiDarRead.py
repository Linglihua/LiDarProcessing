# -*- coding: UTF-8 -*-
'''
@Project ：LiDarProcessing 
@File    ：LiDarRead.py
@Author  ：Xin Zheng
@Date    ：2021/9/16 10:00 
'''

import laspy
import numpy as np
from scipy import spatial

def LidarRead():
    lasFile = r"E:/data/LiDar/self/LidarGuo/read.las"
    inFile = laspy.read(lasFile)
    x, y ,z = inFile.x, inFile.y, inFile.z
    classfication = inFile.classification
    return_num = inFile.return_num
    scan_angle_rank = inFile.scan_angle_rank
    lasdata = np.vstack((x, y, z)).transpose()
    tree = spatial.cKDTree(lasdata)
    aa = tree.query(np.array([323000, 4102252]), 1)
    print(x[aa], y[aa])
    neighbors_distance, neighbors_indices = tree.query(lasdata[100], k=5)  #要返回的第 k 个最近邻居的列表
    print(neighbors_indices)
    print(neighbors_distance)


if __name__ == "__main__":
    LidarRead()