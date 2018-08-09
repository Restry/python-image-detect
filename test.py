#!/usr/bin/python
# coding:utf-8

import os
import glob
from PIL import Image
import colorsys
import math
import diff_color
from tools import deserialization, serialization, addTransparency, cut_by_ratio
import random


def get_dominant_color(image):
    # 颜色模式转换，以便输出rgb颜色值
    # image = image.convert('RGBA')
    image = image.resize((10, 10))
    color = image.getpixel((0, 0))
    return color


# 颜色库
colorStorage = []


def filter_list(list, key, value, limit=None):
    return [i for i in list if i[key] == value][:limit]


def getSimilarImage(color):
    squareColors = []
    colors = []

    for piece in colorStorage:  # 生成颜色匹配值列表
        diff = diff_color.compareColor(color, piece['color'])
        squareColors.append({
            'diff': diff,
            'path': piece['path']
        })
        colors.append(diff)
    
    colors.sort()
    minColor = colors[random.randint(0,10)]

    res = filter_list(squareColors, 'diff', minColor)

    return res[0]['path']


def squareCreation(filePath):
    img = Image.open(filePath).convert('RGB')

    cutCount = 30
    squareSize = (30, 30)

    numColsToCut = math.ceil(img.width / cutCount)
    numRowsToCut = math.ceil(img.height / cutCount)
    widthOfOnePiece = math.ceil(img.width / numColsToCut)
    heightOfOnePiece = math.ceil(img.height / numRowsToCut)
    pieceOfImage = []

    print("分辨率:{0}x{1},分块大小:{2}x{3}".format(numRowsToCut,
                                            numColsToCut, widthOfOnePiece, heightOfOnePiece))

    newImage = Image.open(filePath).resize((img.size[0]*2,img.size[1]*2 ))  # Image.new('RGB', img.size)
    for x in range(0, numColsToCut):
        for y in range(0, numRowsToCut):
            xToCut = x*widthOfOnePiece
            yToCut = y*heightOfOnePiece
            reg = img.crop((
                xToCut,
                yToCut,

                xToCut+widthOfOnePiece,
                yToCut+heightOfOnePiece))
            color = get_dominant_color(reg)

            similarFile = getSimilarImage(color)

            similarImage = Image.open(similarFile).convert('RGB')
            # squareColor = Image.new('RGB', [20, 20], color)
            # similarImage.paste(squareColor, (5, 5))

            # similarImage.thumbnail(reg.size)

            # pieceOfImage.append(similarImage)
            cutedImg = cut_by_ratio(similarImage, (reg.size[0]*2,reg.size[1]*2))
            transImage = addTransparency(cutedImg, factor=0.5)
            
            pieceOfImage.append(transImage)

            r, g, b, a = transImage.split()
            newImage.paste(transImage, (x*transImage.width, y * transImage.height), mask=a)



        print("当前进度:{}%".format(math.ceil(x/(numColsToCut)*100)))

    # reSpliceImage()


    # y = 0
    # maxRow = max([numRowsToCut,numColsToCut])
    # for index in range(len(pieceOfImage)):
    #     piece = pieceOfImage[index]
    #     x = math.floor(index/maxRow)
    #     y = 0 if index % maxRow == 0 else y
    #     r, g, b, a = piece.split()
    #     newImage.paste(piece, (x*piece.width, y * piece.height), mask=a)
    #     y += 1

    newImage.show()
    # serialization(pieceOfImage,'pieceMapping.pkl')
    return newImage


if __name__ == "__main__":
    colorStorage = deserialization('color-mapping.pkl')
    img = squareCreation("files/7.jpg")
    img.save("result/7."+str(random.random())+".jpg", "JPEG")

    if(len(colorStorage) > 0):
        print('缓存存在:{}个图片'.format(len(colorStorage)))
