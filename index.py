#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import re
import urllib
import urllib2
import json
import requests
import sys
import socket
# 设置超时
import time

reload(sys)
sys.setdefaultencoding("utf-8")

timeout = 5


class Crawler:
    # 睡眠时长
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0

    # 获取图片url内容等
    # t 下载图片时间间隔
    def __init__(self, t=0.1):
        self.time_sleep = t
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3', 'Accept-Encoding': 'gzip, deflate'}

    # 开始获取
    def __getImages(self, word=r'美女'):
        search = urllib.quote(word)
        # pn int 图片数
        pn = self.__start_amount
        while pn < self.__amount:
            url = 'http://image.baidu.com/search/avatarjson?tn=resultjsonavatarnew&ie=utf-8&word=' + search + '&cg=girl&pn=' + str(
                pn) + '&rn=60&itg=0&z=0&fr=&width=&height=&lm=-1&ic=0&s=0&st=-1&gsm=1e0000001e'
            # 设置header防ban
            try:
                time.sleep(self.time_sleep)
                req = requests.get(url=url, headers=self.headers)
                content = req.content
                data = content.decode('utf8')
                print(url)
            except UnicodeDecodeError as e:
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib2.URLError as e:
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print("-----socket timout:", url)
            else:
                # 解析json
                json_data = json.loads(data)
                self.__saveImage(json_data, word)
                # 读取下一页
                #print ("下载下一页").decode('utf8')
                pn += 60
            finally:
                pass
        print ("下载任务结束").decode('utf8')
        return

    # 保存图片
    def __saveImage(self, json, word):
        word = word.decode('utf8')
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        # 判断名字是否重复，获取图片长度
        self.__counter = len(os.listdir('./' + word)) + 1
        for info in json['imgs']:
            try:
                if self.__downloadImage(info, word) == False:
                    self.__counter -= 1
            except urllib2.HTTPError as urllib_err:
                print(urllib_err)
                pass
            except Exception as err:
                time.sleep(1)
                #print(err)
                #print ("产生未知错误，放弃保存").decode('utf8')
                continue
            finally:
                #print ("小黄图+1,已有" + str(self.__counter) + "张小黄图").decode('utf8')
                self.__counter += 1
        return

    # 下载图片
    def __downloadImage(self, info, word):
        time.sleep(self.time_sleep)
        fix = self.__getFix(info['objURL'])
        print info['objURL']
        filepath = './' + word + '/' + str(self.__counter) + str(fix)
        self.DownImg(info['objURL'], filepath)

    # 获取后缀名
    def __getFix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    # 获取前缀
    def __getPrefix(self, name):
        return name[:name.find('.')]

    # page_number 需要抓取数据页数 总抓取图片数量为 页数x60
    # start_page 起始页数
    def start(self, word, spider_page_num=1, start_page=1):
        self.__start_amount = (start_page - 1) * 60
        self.__amount = spider_page_num * 60 + self.__start_amount
        self.__getImages(word)

    def DownImg(self, imgurl, path):
        req = requests.get(url=imgurl, headers=self.headers)
        ImgData = req.content
        with open(path, 'wb') as ImgWrite:
            ImgWrite.writelines(ImgData)


crawler = Crawler(0.05)
# crawler.start('美女', 1, 2)
crawler.start(r'鹿晗', 3, 3)
#crawler.start(r'卡通', 3, 3)
# crawler.start('帅哥', 5)
