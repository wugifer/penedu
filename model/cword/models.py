#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models


class CwordOne(models.Model):
    """
    单字
    """
    word = models.CharField(max_length=4, verbose_name=u"字")
    seq = models.IntegerField(verbose_name=u"序号")
    size = models.IntegerField(verbose_name=u"笔画")
    level = models.IntegerField(verbose_name=u"级别")

    def __str__(self):
        return '%s:%s' % (self.login, self.name)

    class Meta:
        db_table = "cword"
