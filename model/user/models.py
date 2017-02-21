#!/usr/bin/python
# -*- coding: utf-8 -*-


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

    def verify(self, verify_time, verify_hash, timeout):
        """
        验证密码。数据库中保存 hash = md5(password)

        Args:
            verify_time(str): 生成 verify_hash 的时间，格式为 yyyy-mm-dd hh:mm:ss
            verify_hash(str): md5(verify_time | md5(password))
            timeout(int): verify_time 与系统时间的差异最大值，超过最大值时总是返回验证失败，时间同步模块生效前暂不使用此参数

        Returns:
            bool: True - 密码正确；False - 密码错误或超时
        """
        return hashlib.md5(self.hash) == verify_hash

    class Meta:
        db_table = "user"
