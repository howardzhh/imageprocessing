import numpy as np
import cv2
import math


def calcGrayHist(image):
    '''
    统计像素值
    :param image:
    :return:
    '''
    # 灰度图像的高，宽
    rows, cols = image.shape
    # 存储灰度直方图
    grayHist = np.zeros([256], np.uint64)
    for r in range(rows):
        for c in range(cols):
            grayHist[image[r][c]] += 1
    return grayHist


def threshEntroy(image):
    rows, cols = image.shape
    # 求灰度直方图
    grayHist = calcGrayHist(image)
    # 归一化灰度直方图，即概率直方图
    normGrayHist = grayHist / float(rows * cols)

    # 第一步:计算累加直方图，也称零阶累积矩
    zeroCumuMoment = np.zeros([256], np.float32)
    for k in range(256):
        if k == 0:
            zeroCumuMoment[k] = normGrayHist[k]
        else:
            zeroCumuMoment[k] = zeroCumuMoment[k - 1] + normGrayHist[k]

    # 第二步:计算各个灰度级的熵
    entropy = np.zeros([256], np.float32)
    for k in range(256):
        if k == 0:
            if normGrayHist[k] == 0:
                entropy[k] = 0
            else:
                entropy[k] = -normGrayHist[k] * math.log10(normGrayHist[k])
        else:
            if normGrayHist[k] == 0:
                entropy[k] = entropy[k - 1]
            else:
                entropy[k] = entropy[k - 1] - normGrayHist[k] * math.log10(normGrayHist[k])
    # 第三步:找阈值
    fT = np.zeros([256], np.float32)
    ft1, ft2 = 0.0, 0.0
    totalEntropy = entropy[255]
    for k in range(255):
        # 找最大值
        maxFront = np.max(normGrayHist[0: k + 1])
        maxBack = np.max(normGrayHist[k + 1: 256])
        if (maxFront == 0 or zeroCumuMoment[k] == 0
                or maxFront == 1 or zeroCumuMoment[k] == 1 or totalEntropy == 0):
            ft1 = 0
        else:
            ft1 = entropy[k] / totalEntropy * (math.log10(zeroCumuMoment[k]) / math.log10(maxFront))

        if (maxBack == 0 or 1 - zeroCumuMoment[k] == 0
                or maxBack == 1 or 1 - zeroCumuMoment[k] == 1):
            ft2 = 0
        else:
            if totalEntropy == 0:
                ft2 = (math.log10(1 - zeroCumuMoment[k]) / math.log10(maxBack))
            else:
                ft2 = (1 - entropy[k] / totalEntropy) * (math.log10(1 - zeroCumuMoment[k]) / math.log10(maxBack))
        fT[k] = ft1 + ft2

    # 找最大值的索引，作为得到的阈值
    threshLoc = np.where(fT == np.max(fT))
    thresh = threshLoc[0][0]

    # 阈值处理
    threshold = np.copy(image)
    threshold[threshold > thresh] = 255
    threshold[threshold <= thresh] = 0
    return threshold


if __name__ == '__main__':
    image0 = cv2.imread(r'C:\Users\14599\Desktop\3.png')
    b, g, r = cv2.split(image0)
    img = threshEntroy(g)
    img = cv2.merge([r, img, b])
    cv2.imshow('origin', image0)
    cv2.imshow('deal_image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#https: // blog.csdn.net / shawroad88 / article / details / 87965784