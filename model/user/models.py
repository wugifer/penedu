#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models


class User(models.Model):
    login = models.CharField(max_length=32, verbose_name=u"login")
    password = models.CharField(max_length=32, verbose_name=u"密码")
    name = models.CharField(max_length=32, verbose_name=u"名称")

    def __str__(self):
        return '%s:%s' % (self.login, self.name)

    class Meta:
        db_table = "user"
