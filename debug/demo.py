import itchat, time

DEBUG = False

if not DEBUG:
    @itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
    def text_reply(msg):
        itchat.send('%s: %s'%(msg['Type'], msg['Text']), msg['FromUserName'])

    @itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
    def download_files(msg):
        print 'LOG', msg['Content']
        fileDir = 'files/%s_%s'%(msg['Type'], int(time.time()))
        msg['Text'](fileDir)
        itchat.send('%s received'%msg['Type'], msg['FromUserName'])
        itchat.send('@%s@%s'%('img' if msg['Type'] == 'Picture' else 'fil', fileDir), msg['FromUserName'])

    @itchat.msg_register('Friends')
    def add_friend(msg):
        itchat.add_friend(**msg['Text'])
        itchat.get_contract()
        itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

    @itchat.msg_register(['Picture'], isGroupChat = True)
    def reply_picture(msg):
        fileDir = 'tmp/%s_%s'%(msg['Type'], int(time.time()))
        msg['Text'](fileDir)
        itchat.send('@img@%s'%fileDir, msg['FromUserName'])

    @itchat.msg_register('Text', isGroupChat = True)
    def text_reply(msg):
        #if msg['isAt']:
        itchat.send(u'@%s\u2005 %s'%(msg['ActualNickName'], msg['Content']), msg['FromUserName'])
else:
    @itchat.msg_register
    def log(msg):
        print 'RECIEVE:', msg['FromUserName'], 'TYPE:', msg['Type'], 'CONTENT:', msg['Content']

itchat.auto_login(hotReload=True)
itchat.run()
