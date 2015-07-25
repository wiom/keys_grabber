#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mechanize import Browser
from lxml import etree
from subprocess import Popen, PIPE

import time, cookielib
import progressbar, webbrowser, re

def showMessage(msg, title = 'htmlParser'):
    #Popen('notify-send "'+title+'" "'+msg+'"', shell= True, stdin= PIPE, stdout= PIPE).stdout.read().split()
    print msg

def max_page(html_doc):
    tree= etree.HTML(html_doc)
    result = tree.xpath(".//*[@id='board_index']/div[1]/div/div[2]/ol/li[1]/a/text()")
    maxPage = result[0][-2] + result[0][-1]
    return maxPage

def rw_file(data = []):
    fileName = '/home/qwerty/workspace/htmlParser/data.txt'
    if len(data) > 0:
        f = open(fileName, 'a')
        for index in data:
            f.write(index + '\n')
    else:
        f = open(fileName, 'r')
        data = [line.strip() for line in f]
    f.close()
    return data

def get_all_keys(html_doc):
    oldKeys = rw_file()
    #.//blockquote/p/span[@class="texthide"]/text()
    tree = etree.HTML(html_doc)
    keysList = tree.xpath('.//blockquote/p/span[@class="texthide"]/text()')
    newKeys = []

    buf = ' '.join(keysList)
    buf = re.sub(r'\s+', ',', buf)
    keysList = buf.split(',')
    print keysList
    for key in keysList:
        if not key in oldKeys:
            #print 'Найден новый ключ %s' % (key)
            newKeys.append(key)

    if len(newKeys) > 0:
        rw_file(newKeys)
        showMessage('На сайте появились новые ключи')
        return True
    else:
        showMessage('Новых ключей не найдено')
        return False

def login_url(
                url,
                login,
                passwd,
                form_nomber,
                login_name,
                paswd_name,
                submit_nomber
            ):
    br = Browser(); showMessage('Создаю интерфейс браузера')
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    br.open(url); showMessage('Загружаю сайт и произвожу вход')
    br.select_form(nr = form_nomber)
    br[login_name] = login
    br[paswd_name] = passwd

    res = br.submit(nr = submit_nomber)
    content = res.read()
    #определить число страниц
    maxPage = int(max_page(content)); showMessage('Определяю количество страниц и перехожу на последнюю')
    curPage = 84
    while curPage < maxPage:
        res = br.open('http://forum.rsload.net/cat-kryaki-seriyniki-varez/topic-4820-page-%d.html' % (maxPage))
        curPage = maxPage
        maxPage = int(max_page(content))
        content = res.read()
    #парсинг ключей
    if get_all_keys(content):
        webbrowser.open_new_tab('http://forum.rsload.net/cat-kryaki-seriyniki-varez/topic-4820-page-%d.html' % (maxPage)) # Вернет True и откроет вкладку

def time_left(curTime):
    return time.time() - curTime

showMessage('Started')
login_url(
            'http://forum.rsload.net/cat-kryaki-seriyniki-varez/topic-4820-page-84.html',
            'wiom',
            'ghbphfr1',
            0,
            'name',
            'password',
            0
        )
curentTime = time.time()
progress = progressbar.ProgressBar(maxval=1800.0).start()
while 1:
    #os.system("clear")
    timeLeft = time_left(curentTime)
    if timeLeft >= 1800.0:
        login_url(
                    'http://forum.rsload.net/cat-kryaki-seriyniki-varez/topic-4820-page-84.html',
                    'wiom',
                    'ghbphfr1',
                    0,
                    'name',
                    'password',
                    0
                )
        curentTime = time.time()
    else:
        progress.update(timeLeft)
progress.finish()
showMessage('Stopped')
