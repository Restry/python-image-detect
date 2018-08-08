# create thumbnail

import os
import glob
from PIL import Image


def cutFile(filePath):
    im = Image.open(filePath).convert('RGB')
    img_size = im.size

    w = img_size[0]
    h = img_size[1]
    print("图片宽度和高度分别是{}".format(img_size))
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


size = (128, 128)
i = 0
folder = "./downloads/高圆圆"
folderTumn = "./downloads/tumn/高圆圆"
if not os.path.exists(folderTumn):
    os.mkdir(folderTumn)
for infile in glob.glob(folder+"/*.jpg"):
    f, ext = os.path.splitext(infile)
    try:
      img = cutFile(infile)
      img.thumbnail(size, Image.ANTIALIAS)
      img.save( folderTumn+"/"+str(i)+".jpg", "JPEG")
    except IOError:
      print("Error: 没有找到文件或读取文件失败"+infile)

    i += 1
