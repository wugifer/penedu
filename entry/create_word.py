#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from contextlib import closing
from pyquery import PyQuery as pq

if __name__ == '__main__':
    seq = 0
    for high in range(0xb0, 0xf8):
        for low in range(0xa1, 0xff):
            seq += 1
            if seq >= 3756 and seq <= 3760:
                continue
            s = '%c%c' % (high, low)
            s = s.decode('gb2312')
            s2 = s.encode('utf-8')
            print seq, s, ','.join([ord(x).__hex__() for x in s]), ','.join([ord(x).__hex__() for x in s2])

    # 构造链接
    high = 0xb0
    low = 0xa1
    s = ('%c%c' % (high, low)).decode('gb2312').encode('utf-8')
    s = ''.join(['%' + ord(x).__hex__()[2:] for x in s])

    # 网络读取
    with closing(urllib2.urlopen('http://www.zdic.net/sousuo/?q=%s' % s.upper())) as conn:
        text = conn.read()

    print text

    print s
