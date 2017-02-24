#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
基于 pyttsx 项目，增加保存成 wav 文件的能力。基本用法： ::

    import sys
    import pyttsx
    from ttsave import save

    # 支持中文需要
    reload(sys)
    sys.setdefaultencoding('utf8')

    # 初始化
    engine = pyttsx.init()

    # 控制语速，不是必须的
    # SAPI 要求在 x=-10~10 之间的整数，10 最快，engine 提供 y = 156.63 * 1.1^x
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate + 50)

    # 控制音量，不是必须的
    # SAPI 要求在 x=0~100 之间的整数，100 最大，engine 提供 0~1 之间的小数，y = 0.01 x
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume - 0.25)

    # 选择语音，不是必须的，windows 7 支持两种，都是女声
    # voices = engine.getProperty('voices')
    for voice in voices:
        # print voice.id, voice.age, voice.gender, voice.languages, voice.name
        engine.setProperty('voice', voice.id)

    # 输出，当然也不是必须的
    engine.say(u'The quick brown fox jumped over the lazy dog.', name='fox')
    engine.say(u'你好！')
    save(engine, 'test.wav', u'The quick brown fox jumped over the lazy dog.')

    # 执行之前的命令，必须的；在 runAndWait 之前，set、say、save 都不起作用
    engine.runAndWait()
"""

import win32com


def save(engine, filename, text):
    """
    把文本对应的语音保存为 .wav 音频文件。仿照 DriverProxy.say 实现

    Args:
        engine (Engine): tts 引擎
        filename (str): 文件名
        text (unicode): 文本，支持中文
    """
    engine.proxy._push(_save, (engine.proxy._driver, filename, text,), None)


def _save(proxy, filename, text):
    """
    执行 rec 指令，仿照 SAPI5Driver.say 实现，注意 Speak 的参数从 19 改为 18，同步模式
    """

    # proxy._proxy.setBusy(True)    # 同步模式，没有回调，不能 setBusy
    proxy._proxy.notify('started-utterance')
    proxy._speaking = True

    fs = win32com.client.Dispatch('SAPI.SpFileStream')
    fs.Open(filename, 3)
    proxy._tts.AudioOutputStream = fs

    proxy._tts.Speak(unicode(text), 18)
    fs.Close()
