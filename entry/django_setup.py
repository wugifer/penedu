#!/usr/bin/python
# -*- coding: utf-8 -*-


import hashlib
import os

import django
from django.conf import settings

INSTALLED_APPS = [
    'model.user',
]


class SQLRouter(object):
    def db_for_read(self, model, **hints):
        config = Config.instance
        if config.CASE == 'True':
            return 'case'
        elif config.TEST == 'True':
            return 'test'
        else:
            return 'dev'

    def db_for_write(self, model, **hints):
        config = Config.instance
        if config.CASE == 'True':
            return 'case'
        elif config.TEST == 'True':
            return 'test'
        else:
            return 'dev'


def create_django_setup():
    return '\n'.join([
        'if __name__ == \'__main__\':',
        '    from entry.django_setup import django_setup',
        '',
        '    django_setup()',
    ])


def django_setup():
    """
    django 环境设置
    """

    if not settings.configured:
        # 三种环境下的 sql 设置
        basic_sql = {
            'ENGINE': 'django.db.backends.sqlite3',
        }

        dev_sql = {'NAME': os.path.abspath(os.path.realpath(__file__ + '/../../db/dev.db'))}
        dev_sql.update(basic_sql)

        case_sql = {'NAME': os.path.abspath(os.path.realpath(__file__ + '/../../db/case.db'))}
        case_sql.update(basic_sql)

        test_sql = {'NAME': os.path.abspath(os.path.realpath(__file__ + '/../../db/test.db'))}
        test_sql.update(basic_sql)

        DATABASES = {
            'dev': dev_sql,
            'case': case_sql,
            'test': test_sql,
            'default': dev_sql
        }

        # 生成 SECRET_KEY 的代码：
        SECRET_KEY = hashlib.md5(os.urandom(16)).hexdigest()

        settings.configure(
            DATABASES=DATABASES,
            DATABASE_ROUTERS=['entry.django_setup.SQLRouter'],
            INSTALLED_APPS=INSTALLED_APPS,
            SECRET_KEY=SECRET_KEY,
            DEBUG=True
        )

        # django 设置
        django.setup()
