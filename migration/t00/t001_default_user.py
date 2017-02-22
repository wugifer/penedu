#!/usr/bin/python
# -*- coding: utf-8 -*-

from model.user.models import User


def up():
    User.objects.create(login='test', hash='e10adc3949ba59abbe56e057f20f883e', name='test')


def down():
    User.objects.all().delete()
