#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from lxml import etree

import cookielib, re

class check_keys():
    def __init__(self):
        #инициализация
        #variables
        self.log_file = ''
        self.keys = []
        self.url = 'http://forum.rsload.net/cat-kryaki-seriyniki-varez/topic-4820-page-%d.html'
        self.login = 'wiom'
        self.passwd = 'ghbphfr1'
        self.form_nomber = 0
        self.login_name = 'name'
        self.paswd_name = 'password'
        self.submit_nomber = 0
        self.curPage = 84
        self.html_source = ''

        self.headers = [(
                        'User-agent',
                        'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'
                        )]

        self.xpath_data = {
                            "max_page" : ".//*[@id='board_index']/div[1]/div/div[2]/ol/li[1]/a/text()",
                            'keys' : './/blockquote/p/span[@class="texthide"]/text()',
                            "is_login" : ".//*[@id='user_info']/fieldset/dl/dt[1]/a/b/span/text()"
                            }

        self.br = Browser()
        self.cj = cookielib.LWPCookieJar()
        self.br.set_cookiejar(self.cj)
        self.br.addheaders = self.headers

    def __del__(self):
        #уничтожение класса
        self.br.close()
        return

    def max_page(self):
        tree= etree.HTML(self.html_source)
        result = tree.xpath(self.xpath_data["max_page"])
        maxPage = result[0][-2] + result[0][-1]
        return maxPage

    def rw_file(self, data = []):
        if len(data) > 0:
            f = open(self.log_file, 'a')
            for index in data:
                f.write(index + '\n')
        else:
            f = open(self.log_file, 'r')
            data = [line.strip() for line in f]
        f.close()
        return data

    def get_all_keys(self):
        oldKeys = self.rw_file()
        tree = etree.HTML(self.html_source)
        keysList = tree.xpath(self.xpath_data["keys"])
        newKeys = []

        buf = ' '.join(keysList)
        buf = re.sub(r'\s+', ',', buf)
        keysList = buf.split(',')

        for key in keysList:
            if not key in oldKeys and key.startswith("CHZ"):
                newKeys.append(key)

        if len(newKeys) > 0:
            self.keys = list(newKeys)
            self.rw_file(newKeys)
            return True
        else:
            return False

    def is_login(self):
        tree= etree.HTML(self.html_source)
        result = tree.xpath(self.xpath_data["is_login"])
        if len(result) == 1:
            return self.login == result[0]
        else:
            return False

    def update(self):
        self.html_source = self.br.open(self.url % (self.curPage)).read()
        maxPage = int(self.max_page())
        if self.curPage != maxPage:
            self.html_source = self.br.open(self.url % (maxPage)).read()
            self.curPage = maxPage
        return self.is_login()


    def login_url(self):
        self.br.open(self.url % (self.curPage))
        self.br.select_form(nr = self.form_nomber)
        self.br[self.login_name] = self.login
        self.br[self.paswd_name] = self.passwd

        self.html_source = self.br.submit(nr = self.submit_nomber).read()
        return self.is_login()

