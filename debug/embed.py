import itchat, time, IPython
@itchat.msg_register
def log(msg):
    print 'RECIEVE:', msg['FromUserName'], 'TYPE:', msg['Type'], 'CONTENT:', msg['Content']
    if msg['Type'] == 'Init':
        return
    IPython.embed()

itchat.auto_login(hotReload=True)
itchat.run()
