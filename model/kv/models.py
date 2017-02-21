#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models


class Kv(models.Model):
    """
    key-value 值对，主要用于配置及其它少量信息记录
    """
    group = models.CharField(max_length=32, verbose_name=u"组")
    key = models.CharField(max_length=32, verbose_name=u"键")
    v = models.CharField(max_length=128, null=True, verbose_name=u"值")
    n = models.IntegerField(null=True, verbose_name=u'值')

    def __str__(self):
        return '%s-%s: %s' % (self.group, self.key, self.v or str(self.n))

    class Meta:
        db_table = "kv"
