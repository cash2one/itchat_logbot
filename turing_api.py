#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: turing_api.py
# Author: Sibo Jia <sibojia.cs@gmail.com>
import requests, os
from common import *

class TuringAPI(object):
	'''provides q&a api by www.tuling123.com'''

	def __init__(self, **args):
		self.path_url = 'http://www.tuling123.com/openapi/api'
		if args.has_key('key_path'):
			self.key = open(args['key_path']).read().strip()

	def get(self, **args):
		query = args.get('query', u'')
		user_hash = args.get('user_hash', u'bot_default')
		try:
			res = requests.post(self.path_url, data = {'key':self.key, 'userid': user_hash, 'info': query.encode('utf8')})
			res = res.json()
			msg = ''
			if res['code'] == 100000: # 文字类
				msg = res['text']
			elif res['code'] == 200000: # 链接类
				msg = res['text'] + ' ' + res['url']
			elif res['code'] == 302000: # 新闻
				for item in res['list']:
					msg += '%s %s %s' % (item['article'] + item['source'] + item['detailurl'])
			elif res['code'] == 308000: # 菜谱
				msg = u'懒得解析菜谱信息'
			elif res['code'] == 40004: # 次数超出限制 免费版5000/天
				msg = u'我好累，说不动了'
			return msg
		except Exception as e:
			print e
			return u'思维脱线中……'

if __name__ == '__main__':
	api = TuringAPI(key_path = os.path.join(script_path(), 'turing_api.key'))
	while True:
		print "Please input query"
		s = raw_input().strip()
		print api.get(s.decode('utf8'))
