#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: logbot.py
# Author: Sibo Jia <sibojia.cs@gmail.com>
import itchat, time, os, sys, random, re
from common import *
from turing_api import TuringAPI
import config as CONFIG

class RandomText(object):
    """get a random line from file"""
    def __init__(self, path):
        super(RandomText, self).__init__()
        self.path = os.path.join(script_path(), path)
        if os.path.exists(self.path):
            self.lines = open(self.path).read().splitlines()
        else:
            self.lines = []

    def get(self, **args):
        if len(self.lines) > 0:
            return random.choice(self.lines).decode('utf8')
        else:
            return ''

chat_text_gen = RandomText('random_text.txt')
turing_api = TuringAPI(key_path = os.path.join(script_path(), 'turing_api.key'))

class Utils(object):
    '''utils for itchat'''
    contract_name_dict = {}
    logger_dict = {}
    class TextLogger(object):
        """Logs text to screen and file"""
        def __init__(self, path):
            super(Utils.TextLogger, self).__init__()
            self.set_path(path)

        def set_path(self, path):
            p=os.path.join(script_path(), path)
            self.fout = open(p, 'a')

        def log(self, msg, isGroupChat = False, contentOverride = None):
            timestr = Utils.get_time_str(msg)
            if isGroupChat:
                name = msg['ActualNickName']
            else:
                name = Utils.get_username(msg['FromUserName'])
            if contentOverride:
                content = contentOverride
            else:
                content = msg['Content']
            logstr = u'%s|%s|%s\n' % (timestr, name, content)
            self.fout.write(logstr.encode('utf8'))
            self.fout.flush()
            print logstr,

        def log_raw(self, msg):
            logstr = u'%s|%s\n' % (time.strftime('%Y-%m-%d-%H-%M-%S'), msg)
            self.fout.write(logstr.encode('utf8'))
            self.fout.flush()
            print logstr,

    @classmethod
    def get_logger(cls, fromusername, isGroupChat = False):
        name = Utils.get_username(fromusername)
        if not cls.logger_dict.has_key(name):
            if isGroupChat:
                rel_path = os.path.join(u'log_groupchat', u'%s.txt' % name)
            else:
                rel_path = os.path.join(u'log_chat', u'%s.txt' % name)
            logger = Utils.TextLogger(rel_path)
            cls.logger_dict[name] = logger
        return cls.logger_dict[name]

    @classmethod
    def get_username(cls, fromusername):
        try:
            tryname = itchat.get_batch_contract(fromusername)['NickName']
            if len(tryname) > 0:
                return tryname
            else:
                return 'Nobody'
        except:
            return 'Nobody'
        # def _build_dict(update=False):
        #     d = itchat.get_contract(update)
        #     for item in d:
        #         cls.contract_name_dict[item['UserName']] = item['NickName']
        # if not cls.contract_name_dict.has_key(fromusername):
        #     _build_dict()
        # if not cls.contract_name_dict.has_key(fromusername):
        #     _build_dict(True)
        # if cls.contract_name_dict.has_key(fromusername):
        #     return cls.contract_name_dict[fromusername]
        # else:
        #     return 'Nobody'

    @staticmethod
    def get_time_str(msg):
        t=time.localtime(msg['CreateTime'])
        return time.strftime('%Y-%m-%d-%H-%M-%S',t)

@itchat.msg_register(['Text'])
def text_reply(msg):
    Utils.get_logger(msg['FromUserName']).log(msg)
    if CONFIG.reply_engine == 'random':
        send_msg = chat_text_gen.get()
    elif CONFIG.reply_engine == 'turing':
        send_msg = turing_api.get(query = msg['Text'], user_hash = msg['FromUserName'][:20])
    Utils.get_logger(msg['FromUserName']).log_raw(send_msg)
    itchat.send(send_msg, msg['FromUserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def download_files(msg):
    content = '%s %s received and saved' % (msg['Type'], msg['FileName'])
    Utils.get_logger(msg['FromUserName']).log(msg, contentOverride = content)
    fileDir = 'files_download/%s_%s_%s' % (Utils.get_time_str(msg), Utils.get_username(msg['FromUserName']), msg['FileName'])
    msg['Text'](fileDir)
    itchat.send(content, msg['FromUserName'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.get_contract(True)
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'], isGroupChat = True)
def download_files_group(msg):
    content = '%s %s received and saved' % (msg['Type'], msg['FileName'])
    Utils.get_logger(msg['FromUserName'], isGroupChat = True).log(msg, contentOverride = content)
    fileDir = 'files_download/%s_%s_%s_%s' % (Utils.get_time_str(msg),
        Utils.get_username(msg['FromUserName']), msg['ActualNickName'], msg['FileName'])
    msg['Text'](fileDir)

@itchat.msg_register('Sharing', isGroupChat = True)
def log_share_group(msg):
    content = u'URL:"%s" TITLE:"%s"' % (msg['Url'], msg['Text'])
    Utils.get_logger(msg['FromUserName'], isGroupChat = True).log(msg, contentOverride = content, isGroupChat = True)

@itchat.msg_register('Text', isGroupChat = True)
def text_reply_group(msg):
    Utils.get_logger(msg['FromUserName'], isGroupChat = True).log(msg, isGroupChat = True)
    if msg['isAt']:
        if CONFIG.reply_engine == 'random':
            send_msg = chat_text_gen.get()
        elif CONFIG.reply_engine == 'turing':
            rep = re.sub(ur'@.*?\u2005', '', msg['Text'])
            send_msg = turing_api.get(query = rep, user_hash = msg['FromUserName'][:20])
        Utils.get_logger(msg['FromUserName'], isGroupChat = True).log_raw(send_msg)
        itchat.send(u'@%s\u2005 %s'%(msg['ActualNickName'], send_msg), msg['FromUserName'])

itchat.auto_login(hotReload=True)
itchat.run()
itchat.dump_login_status()
