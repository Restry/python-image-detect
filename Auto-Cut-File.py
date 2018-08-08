# create thumbnail

import os
import glob
from PIL import Image
import colorsys


def get_dominant_color(image):

    # 颜色模式转换，以便输出rgb颜色值
    #image = image.convert('RGBA')

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


size = (128, 128)
i = 0

sourcesFolder = "downloads/sources"
thumbnailFolder = "downloads/thumbnail"

for folder in os.listdir('downloads/sources'):
    t_folder = thumbnailFolder+"/"+folder
    if not os.path.exists(t_folder):
        os.mkdir(t_folder)

    print('处理:{}中'.format(folder))

    for infile in glob.glob(sourcesFolder+"/"+folder+"/*.jpg"):
        f, ext = os.path.splitext(infile)
        try:
            img = cutFile(infile)
            img.thumbnail(size, Image.ANTIALIAS)
            color = get_dominant_color(img)
            print("图片色值:{}".format(color))
            # # img= img.convert('RGB')
            # print(img)
            # print(p)
            # # p.show()
            t_save_file = t_folder+"/"+str(i)+".jpg"

            p = Image.new('RGB', [50, 20], color)
            img.paste(p, (5, 5))
            #p.save(t_folder+"/"+str(i)+".c.jpg")
            img.save(t_save_file, "JPEG")

        except IOError:
            print("Error: 没有找到文件或读取文件失败"+infile)

        i += 1
