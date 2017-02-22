#!/usr/bin/python
# -*- coding: utf-8 -*-


import datetime
import hashlib

from django.db import models


class User(models.Model):
    """
    用户
    """
    login = models.CharField(max_length=32, verbose_name=u"login")
    hash = models.CharField(max_length=32, verbose_name=u"摘要")
    name = models.CharField(max_length=32, verbose_name=u"名称")

    def __str__(self):
        return '%s:%s' % (self.login, self.name)

    def verify(self, verify_hash, timeout):
        """
        验证密码。数据库中保存 hash = md5(password)

        Args:
            verify_hash(str): md5(verify_time | md5(password))，verify_time 是生成 verify_hash 的时间，格式为 yyyy-mm-dd hh:mm
            timeout(int): verify_time 与系统时间的差异最大值（分钟），超过最大值时总是返回验证失败，时间同步模块生效前暂不使用此参数

        Returns:
            bool: True - 密码正确；False - 密码错误或超时
        """
        now = datetime.datetime.now()
        for diff in (range(0, timeout + 1) + range(-1, -(timeout + 1), -1)):
            now_str = (now + datetime.timedelta(minutes=diff)).strftime('%Y-%m-%d %H:%M')
            if hashlib.md5(now_str + '%s' % self.hash).hexdigest() == verify_hash:
                return True

        return False

    class Meta:
        db_table = "user"
