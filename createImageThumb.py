#!/usr/bin/python
# coding:utf-8

import os
import glob
from PIL import Image
import colorsys
import math
from tools import deserialization, serialization, rgb_to_10
from db import createDB


def get_dominant_color(image):

        # 颜色模式转换，以便输出rgb颜色值
        # image = image.convert('RGBA')

    image = image.resize((10, 10))
    color = image.getpixel((0, 0))
    return color
    # 生成缩略图，减少计算量，减小cpu压力
    # image.thumbnail((200, 200))

    # max_score = 0  # 原来的代码此处为None
    # # 原来的代码此处为None，但运行出错，改为0以后 运行成功，原因在于在下面的 score > max_score的比较中，max_score的初始格式不定
    # dominant_color = 0

    # for count, (r, g, b, a) in image.getcolors(image.size[0] * image.size[1]):
    #     # 跳过纯黑色
    #     if a == 0:
    #         continue

    #     saturation = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)[1]

    #     y = min(abs(r * 2104 + g * 4130 + b * 802 + 4096 + 131072) >> 13, 235)

    #     y = (y - 16.0) / (235 - 16)

    #     # 忽略高亮色
    #     if y > 0.9:
    #         continue

    #     # Calculate the score, preferring highly saturated colors.
    #     # Add 0.1 to the saturation so we don't completely ignore grayscale
    #     # colors by multiplying the count by zero, but still give them a low
    #     # weight.
    #     score = (saturation + 0.1) * count

    #     if score > max_score:
    #         max_score = score
    #         dominant_color = (r, g, b)

    # return dominant_color


def cutFile(filePath):
    im = Image.open(filePath).convert('RGB')
    img_size = im.size

    w = img_size[0]
    h = img_size[1]

    x = 0
    y = 0
    vw = h if w > h else w
    vh = vw
    # print("尝试指定裁剪宽{0},高{1}".format(vw, vh))
    x = w/4
    y = h/4
    # print("x:{0},y:{1}".format(x, y))

    x = 0 if (x+vw) > w else x
    y = 0 if (y+vh) > h else y
    # print("修正后,x:{0},y:{1}".format(x, y))
    # print("尝试指定裁剪宽{0},高{1}".format(vw, vh))

    reg = im.crop((x, y, x+vw, y+vh))
    # reg.show()
    return reg


(conn, c) = createDB()


def insertToDB(row):
    c.execute("INSERT INTO images VALUES ({0},{1},{2},'{3}',{4},{5},{6},'{7}','{8}')".format(row['r'],
                                                                                             row['g'],
                                                                                             row['b'],
                                                                                             row['path'],
                                                                                             row['color'],
                                                                                             row['width'],
                                                                                             row['height'],
                                                                                             row['name'],
                                                                                             row['originPath']))
    pass


def originalProcess(path, thumbPath):
    i = 0
    if not os.path.exists(thumbPath):
        os.mkdir(thumbPath)

    for folder in os.listdir(path):
        t_folder = thumbPath+"/"+folder
        if not os.path.exists(t_folder):
            os.mkdir(t_folder)

        print('处理{}中...'.format(folder))

        for infile in glob.glob(sourcesFolder+"/"+folder+"/*.*"):
            f, ext = os.path.splitext(infile)
            try:
                img = cutFile(infile)
                img = img.resize(size)
                color = get_dominant_color(img)
                # print("图片色值:{}".format(color))

                t_save_file = t_folder+"/"+str(i)+'.jpg'

                p = Image.new('RGB', [50, 20], color)
                # img.paste(p, (5, 5))  取消上色

                # p.save(t_folder+"/"+str(i)+".c.jpg")
                img.save(t_save_file, "JPEG")

                colorStorage.append({'color': color, 'path': t_save_file})

                insertToDB({
                    'r': color[0],
                    'g': color[1],
                    'b': color[2],
                    'color': rgb_to_10(color),
                    'width': img.width,
                    'height': img.height,
                    'path': t_save_file,
                    'name': folder,
                    'originPath': infile
                })

            except Exception as e:
                print("Error: 读取文件失败:%s %s" % (infile, e))

            i += 1


size = (300, 300)  # 生成小图尺寸

sourcesFolder = "downloads/sources"
thumbnailFolder = "downloads/thumbnail"

colorStorage = deserialization('color-mapping.pkl')

if(len(colorStorage) > 0):
    print('缓存存在:{}个图片'.format(len(colorStorage)))
else:
    originalProcess(sourcesFolder, thumbnailFolder)
    print('获取到:{}个图片,准备生成缓存插入数据库'.format(len(colorStorage)))
    serialization(colorStorage, 'result/color-mapping.pkl')

    for row in c.execute("select count(*) from images"):
        print(row)

    conn.commit()
    conn.close()


print("完成! 一共有{0}个图片".format(len(colorStorage)))
