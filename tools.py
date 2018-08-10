import pickle
import os
from PIL import Image

import struct

# RGB元素范围(0-1)


def hex_to_rgb(hex_str):
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))
    return tuple([val/255 for val in int_tuple])

# print(hex_to_rgb('7BF5BE'))


# RGB元素范围(0-255)
def hex2rgb(hex_str):
    int_tuple = struct.unpack('BBB', bytes.fromhex(hex_str))
    return tuple([val for val in int_tuple])

# print(hex2rgb('7BF5BE'))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def rgb_to_10(rgb):
    return int('%02x%02x%02x' % rgb, 16)

# rgb = (123, 23, 34)
# print(rgb_to_hex(rgb))


def serialization(obj, file='color-mapping.pkl'):
    with open(file, 'wb') as f:
        pickle.dump(obj, f)


def deserialization(file='color-mapping.pkl'):
    if os.path.exists(file):
        with open(file, 'rb') as f:
            return pickle.load(f)
    else:
        return []


def addTransparency(img, factor=0.7):
    img = img.convert('RGBA')
    img_blender = Image.new('RGBA', img.size, (0, 0, 0, 0))
    img = Image.blend(img_blender, img, factor)
    return img


def cut_by_ratio(im, size):
    """按照图片长宽比进行分割"""
    # im = Image.open(cls.infile)

    width = float(size[0])
    height = float(size[1])
    (x, y) = im.size
    crop_img = im

    # if width > height:
    #     region = (0, int((y-(y * (height / width)))/2),
    #               x, int((y+(y * (height / width)))/2))
    #     crop_img = im.crop(region)
    # elif width < height:
    #     region = (int((x-(x * (width / height)))/2), 0,
    #               int((x+(x * (width / height)))/2), y)
    #     crop_img = im.crop(region)
    # else:
    #     crop_img = im.resize(size)
    # 裁切图片
    return im.resize(size)


# # coding=utf-8
# import Image
# import shutil
# import os


# class Graphics:
#     infile = 'D:\\myimg.jpg'
#     outfile = 'D:\\adjust_img.jpg'

#     @classmethod
#     def fixed_size(cls, width, height):
#         """按照固定尺寸处理图片"""
#         im = Image.open(cls.infile)
#         out = im.resize((width, height),Image.ANTIALIAS)
#         out.save(cls.outfile)

#     @classmethod
#     def resize_by_width(cls, w_divide_h):
#         """按照宽度进行所需比例缩放"""
#         im = Image.open(cls.infile)
#         (x, y) = im.size
#         x_s = x
#         y_s = x/w_divide_h
#         out = im.resize((x_s, y_s), Image.ANTIALIAS)
#         out.save(cls.outfile)

#     @classmethod
#     def resize_by_height(cls, w_divide_h):
#         """按照高度进行所需比例缩放"""
#         im = Image.open(cls.infile)
#         (x, y) = im.size
#         x_s = y*w_divide_h
#         y_s = y
#         out = im.resize((x_s, y_s), Image.ANTIALIAS)
#         out.save(cls.outfile)

#     @classmethod
#     def resize_by_size(cls, size):
#         """按照生成图片文件大小进行处理(单位KB)"""
#         size *= 1024
#         im = Image.open(cls.infile)
#         size_tmp = os.path.getsize(cls.infile)
#         q = 100
#         while size_tmp > size and q > 0:
#             print q
#             out = im.resize(im.size, Image.ANTIALIAS)
#             out.save(cls.outfile, quality=q)
#             size_tmp = os.path.getsize(cls.outfile)
#             q -= 5
#         if q == 100:
#             shutil.copy(cls.infile, cls.outfile)

#     @classmethod
#     def cut_by_ratio(cls, width, height):
#         """按照图片长宽比进行分割"""
#         im = Image.open(cls.infile)
#         width = float(width)
#         height = float(height)
#         (x, y) = im.size
#         if width > height:
#             region = (0, int((y-(y * (height / width)))/2), x, int((y+(y * (height / width)))/2))
#         elif width < height:
#             region = (int((x-(x * (width / height)))/2), 0, int((x+(x * (width / height)))/2), y)
#         else:
#             region = (0, 0, x, y)

#         #裁切图片
#         crop_img = im.crop(region)
#         #保存裁切后的图片
#         crop_img.save(cls.outfile)
