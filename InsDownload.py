#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
proxies = {
    'http': 'http://127.0.0.1:1087',
    'https': 'http://127.0.0.1:1087'
}


def download_single_file(file_url):
    """
    读取url内容，获取url对应的用户图片
    :param file_url:
    :return:
    """
    f = requests.get(file_url, proxies=proxies)
    html_source = f.text
    soup = BeautifulSoup(html_source, 'html.parser')
    meta_tag = soup.find_all('meta', {'property': 'og:image'})
    img_url = meta_tag[0]['content']
    return img_url


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        img_file = download_single_file(url)
        input_text = url
        return render_template('index.html', img_file=img_file, input_text=input_text)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
