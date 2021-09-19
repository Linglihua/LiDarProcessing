# -*- coding: UTF-8 -*-
'''
@Project ：LiDarProcessing 
@File    ：readLas.py
@Author  ：Xin Zheng
@Date    ：2021/9/16 10:55 
'''


import laspy
import numpy as np
import s3fs
import matplotlib.pyplot as plt

lasFile = r"E:/data/LiDar/self/LidarGuo/read.las"
lasFile2 = r"E:/data/LiDar/self/LidarGuo/write1.las"

def readLas(lasF):
    las = laspy.read(lasF)
    print(np.unique(las.classification))    #unique用于返回无重复

#reading just the header and vlrs but not the points,
def read2Las():
    fs = s3fs.S3FileSystem()
    with fs.open(lasFile, 'rb') as f:
        if f.header.point_count < 100_000_000:
            las = laspy.read(f)

#he object returned by the laspy.open() function, LasReader can also be
# used to read points chunk by chunk by using LasReader.chunk_iterator()
def readChunked():
    with laspy.open(lasFile) as las:
        counter = 0
        for points in las.chunk_iterator(int(las.header.point_count/5)):
            counter += 1
        print(counter)

#write
def writeLas():
    las = laspy.read(lasFile)
    las.points[las.classification == 2]
    las.write(r"E:/data/LiDar/self/LidarGuo/write1.las")

    readLas(lasFile2)

def writeChuntked():
    with laspy.open(lasFile) as las:
        with laspy.open(lasFile2, mode = "w", header = las.header) as writer:
            for points in las.chunk_iterator(int(las.header.point_count/5)):
                writer.write_points(points[points.classification == 2])


def creating(points_kept):
    las = laspy.read(lasFile)
    sub_las = laspy.LasData(las.header)
    sub_las.points = points_kept.copy()
    sub_las.write("close_points.las")




def scaled_x_dimension():
    #求实际位置
    las = laspy.read(lasFile)
    x_dmension = las.X
    scale = las.header.scales[0]  #缩放量
    offset = las.header.offset[0] #偏移量
    print(x_dmension * scale + offset)     #实际坐标


    #查看有哪些纬度
    for dimension in las.point_format.dimensions:
        print(dimension.name)

    #
    X_invalid = (las.header.mins[0] > las.x) | (las.header.maxs[0] < las.x)
    Y_invalid = (las.header.mins[1] > las.y) | (las.header.maxs[1] < las.y)
    Z_invalid = (las.header.mins[2] > las.z) | (las.header.maxs[2] < las.z)
    bad_indices = np.where(X_invalid | Y_invalid | Z_invalid)

    print(bad_indices)

    #求距离第一个点一定距离的点
    coords = np.vstack((las.x, las.y, las.z)).transpose() #按照垂直方式堆叠
    first_point = coords[0, :] #第一个点、
    distances = np.sum(np.sqrt((coords - first_point) ** 2), axis = 1) #axis为0是压缩行,axis为1是压缩列
    mask = distances < 5
    points_kept = las.points[mask]
    print("We kept %i points out of %i total" % (len(points_kept), len(las.points)))

    #找出地面点
    ground_points = las.points[las.number_of_returns == las.return_number]

    print("%i points out of %i were ground points." %(len(ground_points), len(las.points)))

    plt.hist(las.intensity)
    plt.title("Histogram of the Intensity Dimension")
    plt.show()

    creating(ground_points)




if __name__ == '__main__':
    #readLas(lasFile)
    #read2Las()
    #readChunked()
    #writeLas()
    scaled_x_dimension()

