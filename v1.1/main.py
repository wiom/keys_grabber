#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
from subprocess import Popen, PIPE

import progressbar
import grabber
from source import checker



# global variables
cwd = os.getcwd()
interval = 60
msg = True
outFile = cwd + '/out.txt'
old_keys = cwd + '/data.txt'
cg_file = cwd + '/cg_logins.txt'
logFile = cwd + '/file to logs'


class do_work():
    def __init__(self, cg_logins_file):
        self.cg_logins_file = cg_logins_file
        self.cg_login = ''
        self.cg_passwd = ''

    def unrun(self):
        # уничтожаем классы
        del self.cg
        del self.rsload
        return True

    def run(self):
        # инициализируем классы
        self.rsload = grabber.check_keys()
        self.rsload.log_file = old_keys
        self.rsload.login_url()

        self.cg = checker.cyberghostvpn()
        self.cg.login(self.cg_login, self.cg_passwd)
        return True

    def mybe_activ(self, key):
        self.cg.key_input_activate()
        self.cg.check_key(key)
        return self.cg.get_alertion_text()

    def check(self):
        # функция для чека ключей
        loop = []
        if self.rsload.update():
            if self.rsload.get_all_keys():
                return self.rsload.keys
            else:
                return loop
        else:
            return loop

    def get_login_cg(self):
        f = open(self.cg_logins_file).readlines()
        if not f:
            return
        login = f.pop(0)
        with open(self.cg_logins_file, 'w') as F:
            F.writelines(f)
        cg_login = login.split(':')
        return cg_login

    def rw_file(self, file_name, data):
        f = open(file_name, 'a')
        for index in data:
            f.write(index + ':')
        f.write('\n')
        f.close()

    def notify(self, msg, title='CG'):
        self.notify = self.normal_notify
        pass

    def normal_notify(self, msg, title='CG'):
        Popen('notify-send "' + title + '" "' + msg + '"',
              shell=True, stdin=PIPE, stdout=PIPE)


def change_cg_login():
    work.notify("%s:%s" % (work.cg_login, work.cg_passwd), "Активирован аккаунт")
    user_data = work.get_login_cg()

    if user_data == None:
        work.notify('Нет данных для авторизации')
        progress.finish()
        work.unrun()
        raise SystemExit(1)

    work.cg_login = user_data[0]
    work.cg_passwd = user_data[1]
    return user_data


progress = progressbar.ProgressBar(maxval=interval)

work = do_work(cg_file)
user_data = change_cg_login()
work.run()

while msg:
    print('\nWaiting... [Hit Ctrl-C to exit]')
    try:
        for i in range(0, interval):
            progress.update(i)
            time.sleep(1)
        print("\nChecking...")

        keys = work.check()
        if keys:
            for cg_key in keys:
                if work.mybe_activ(cg_key):
                    work.cg.reload()
                    work.rw_file(outFile, user_data)
                    user_data = change_cg_login()
                    work.cg.login(user_data[0], user_data[1])
    except KeyboardInterrupt:
        msg = False
progress.finish()
work.unrun()
