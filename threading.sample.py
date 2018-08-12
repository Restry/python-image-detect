# -*- coding: utf-8 -*-
import threading

from PIL import Image

image_size = range(1, 1001)


def start():
  for size in image_size:
    t = threading.Thread(target=create_image, args=(size,))
    t.start()


def create_image(size):
  pri_image = Image.open("origin.png")
  pri_image.resize((size, size), Image.ANTIALIAS).save("img/png_%d.png" % size)


if __name__ == "__main__":
  start()