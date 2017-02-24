#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys

import pyttsx

from libc.ttsave import save

# 支持中文需要
reload(sys)
sys.setdefaultencoding('utf8')

# 初始化
engine = pyttsx.init()

# 控制语速，不是必须的
engine.setProperty('rate', 150.0)

# 控制音量，不是必须的
engine.setProperty('volume', 1.0)

# 选择语音，不是必须的
# voices = engine.getProperty('voices')
# for voice in voices:
#     print voice.id, voice.age, voice.gender, voice.languages, voice.name
#     engine.setProperty('voice', voice.id)

# 输出
# engine.say(u'The quick brown fox jumped over the lazy dog.', name='fox')
# engine.say(u'你好！')
save(engine, '2.wav', u'把今天的记事发给我们，该做作业啦')
save(engine, '3.wav', u'按优先顺序，先做标红的，再做我们布置的作业')
save(engine, '4.wav', u'该弹钢琴了')
save(engine, '5.wav', u'在表格上记录进度，标注已完成项目的序号')
save(engine, '6.wav', u'完成标红作业、家庭作业后，继续完成未标红的作业')

engine.runAndWait()
