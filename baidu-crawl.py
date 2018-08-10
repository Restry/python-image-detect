#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
# 设置超时
import time

import sys
import getopt


def main(argv):
    words = ''
    size = 5
    page = 1
    width = 800
    try:
        opts, args = getopt.getopt(
            argv, "hw:s:p:d:", ["words=", "size=", "page=", "width="])
        print(opts, args)
    except getopt.GetoptError:
        print('test.py -w <关键字> -s <大小> -p <页码> -d <宽度>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -w <关键字> -s <大小> -p <页码> -d <宽度>')
            sys.exit()
        elif opt in ("-w", "--words"):
            words = arg.strip()
        elif opt in ("-s", "--size"):
            size = int(arg.strip())
        elif opt in ("-p", "--page"):
            page = int(arg.strip())
        elif opt in ("-d", "--width"):
            width = int(arg.strip())
    print('关键字:', words)
    print('大小:', size)
    print('页码:', page)
    print('宽度:', width)
    return (words, size, page, width)


timeout = 5
savePath = './downloads/sources/'
socket.setdefaulttimeout(timeout)


class Crawler:
        # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t

    # 获取后缀名
    def get_suffix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取referrer，用于生成referrer
    def get_referrer(self, url):
        par = urllib.parse.urlparse(url)
        if par.scheme:
            return par.scheme + '://' + par.netloc
        else:
            return par.netloc

        # 保存图片
    def save_image(self, rsp_data, word):
        if not os.path.exists(savePath + word):
            os.mkdir(savePath + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir(savePath)) + 1
        for image_info in rsp_data['imgs']:

            try:
                time.sleep(self.time_sleep)
                urlParmas = 'objURL'

                suffix = self.get_suffix(image_info[urlParmas])
                # 指定UA和referrer，减少403
                refer = self.get_referrer(image_info[urlParmas])
                opener = urllib.request.build_opener()
                opener.addheaders = [
                    ('User-agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'),
                    ('Referer', refer)
                ]
                urllib.request.install_opener(opener)
                # 保存图片
                urllib.request.urlretrieve(
                    image_info[urlParmas], savePath + word + '/' + str(self.__counter) + str(suffix))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                print(word+"+1,已有" + str(self.__counter) + "张")
                self.__counter += 1
        return

    # 开始获取
    def get_images(self, word='美女', width=800):
        search = urllib.parse.quote(word)
        # pn int 图片数
        pn = self.__start_amount
        while pn < self.__amount:

            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width='+str(width)+'&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read().decode('unicode_escape')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                # 解析json
                rsp_data = json.loads(rsp)
                self.save_image(rsp_data, word)
                # 读取下一页
                print("下载下一页")
                pn += 60
            finally:
                page.close()
        print("下载任务结束")
        return

    def start(self, word, spider_page_num=5, start_page=1, width=800):
        """
        爬虫入口
        :param word: 抓取的关键词
        :param spider_page_num: 需要抓取数据页数 总抓取图片数量为 页数x60
        :param start_page:起始页数
        :return:
        """
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.get_images(word)


if __name__ == '__main__':
    crawler = Crawler(0.05)  # 抓取延迟为 0.05
    (words, size, page, width) = main(sys.argv[1:]) 

    # 抓取关键词为 “美女”，总数为 1 页（即总共 1*60=60 张），开始页码为 2
    # for item in ['中国红','高级黑','科技','灵感','山水','国画','帅哥']:
    
    for item in ['黄渤','徐峥','王宝强','沈腾','肖央','王太利','石天','王晶','周星驰','吴孟达','郭德纲','陈佩斯','赵本山','小沈阳','岳云鹏','范伟','宋小宝','潘斌龙','大张伟','白凯南','修睿','许冠杰','冯巩','黄百鸣','葛优']:
      print( item)
      crawler.start(item, size, page,  width)

