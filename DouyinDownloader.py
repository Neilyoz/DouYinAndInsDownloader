# coding=utf-8
import requests
import json
import re
import os
import sys
import time
from urllib.parse import urlparse
from contextlib import closing
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class DouYinDownloader(object):
    def __init__(self):
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
        }

        self.domain = ['www.douyin.com', 'v.douyin.com', 'www.snssdk.com',
                       'www.amemv.com', 'www.iesdouyin.com', 'aweme.snssdk.com']

    def hello(self):
        print('*' * 60)
        print('\t\t抖音无水印视频下载')
        print('*' * 60)
        self.run()

    def run(self):
        self.share_url = input('请输入分享链接：')
        # self.share_url = "http://v.douyin.com/LmKj5u/"

        if not self.share_url:
            return self.run()

        self.share_url = self.getLocation()

        share_url_parse = urlparse(self.share_url)

        if not share_url_parse.scheme in ['http', 'https'] or not share_url_parse.netloc in self.domain:
            return self.run()

        html_url = share_url_parse.scheme + "://" + share_url_parse.netloc + \
            share_url_parse.path + "?" + share_url_parse.query

        self.downLoader(html_url)

    def downLoader(self, url):
        response = requests.get(url, headers=self.headers)
        bf = BeautifulSoup(response.text, 'lxml')
        video = bf.find_all('video')
        video_url = video[0].get('src').replace('playwm', 'play')

        print(video_url)

        response = requests.get(
            video_url, headers=self.headers, allow_redirects=False)
        print(response.headers.keys())

        inputs = bf.find_all("input")
        video_name = time.time()

        for item in inputs:
            temp = item.get('name')
            if temp == 'shareDesc':
                video_name = item.get('value')
                break

        size = 0
        with closing(requests.get(video_url, headers=self.headers, stream=True, verify=False)) as response:
            chunk_size = 1024
            content_size = int(response.headers['content-length'])

            if response.status_code == 200:
                sys.stdout.write('  [文件大小]:%0.2f MB %s \n' % (
                    content_size / chunk_size / 1024, video_name + '.mp4'))

                with open(video_name + ".mp4", "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        file.write(data)
                        size += len(data)
                        file.flush()
                        sys.stdout.write('  [下载进度]:%.2f%% %s' % (
                            float(size / content_size * 100), video_name + '.mp4 \r'))
                        sys.stdout.flush()

                sys.stdout.write('\n')

    def getLocation(self):
        response = requests.get(
            self.share_url, headers=self.headers, allow_redirects=False)
        if 'Location' in response.headers.keys():
            return response.headers['Location']
        else:
            return self.share_url


if __name__ == '__main__':
    dy = DouYinDownloader()
    dy.hello()
