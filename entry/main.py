#!/usr/bin/python
# -*- coding: utf-8 -*-


import hashlib
import importlib
import os
import sys

import django
from django.conf import settings

"""
可用入口点数组

每个数组 ['module.a.b', 'c', 'd'] 对应一个入口点，其中第一个参数对应模块，其余参数对应模块 main() 的参数。
入口点从 0 开始排序依次 +1，可以通过在数组前插入整数直接调整入口点的序号
"""
ENTRY_POINTS = [
    ['server.app'],  # entry_id = 0, 固定为执行不带参数的 server.app
    100,
    ['entry.django_manage', 'any.py', 'makemigrations', 'user'],
    ['entry.django_manage', 'any.py', 'migrate'],
    ['entry.django_manage', 'any.py', 'migrate', '--database=case'],
]

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


def main():
    # 设置系统路径
    _set_syspath()

    # 设置入口点
    _compile_entry_point()

    # 设置 django 参数
    _set_django()

    # app reloader 触发再次程序运行，跳过 entry 判断，执行 _exec_entry('0')
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        _exec_module_main(ENTRY_POINTS[0][:-1])

    # 不含参数，从命令行选择入口点
    elif len(sys.argv) == 1:
        _select_and_exec_entry()

    # 第二个参数是整数入口 / 入口
    elif len(sys.argv) == 2:
        _exec_entry(sys.argv[1])

    # 余下参数是入口
    else:
        _exec_module_main(sys.argv[1:])


def _compile_entry_point():
    """
    编译 ENTRY_POINTS
    """

    # entry id 自动编码，从 0 开始
    entry_id = 0
    for entry_point in ENTRY_POINTS:
        # 整数，从下一项开始更新 entry id
        if type(entry_point) == int:
            entry_id = entry_point
        # 数组，把自动编码的 entry id 附加在数组最后
        else:
            entry_point.append(str(entry_id))
            entry_id += 1


def _exec_entry(entry_id_or_list):
    """
    执行 ENTRY_POINT 中的入口点
    """

    # 尝试把 entry_id_or_list 作为 id
    for entry_point in ENTRY_POINTS:
        if type(entry_point) == list and entry_point[-1] == entry_id_or_list:
            _exec_module_main(entry_point[:-1])
            return

    # 把 entry_id_or_list 作为未分割的参数列表
    _exec_module_main(entry_id_or_list.split(' '))


def _exec_module_main(params):
    """
    执行指定模块的 main 函数
    """

    entry_module = importlib.import_module(params[0])
    entry_main = getattr(entry_module, 'main')
    if len(params) == 1:
        entry_main()
    else:
        entry_main(tuple(params[1:]))


def _select_and_exec_entry():
    """
    选择并执行入口
    """

    # 列出可用命令
    print u'可用命令:'
    for entry_point in ENTRY_POINTS:
        if type(entry_point) == list:
            print '  %s: %s' % (entry_point[-1], ' '.join(entry_point[:-1]))

    # 列出操作选项
    print u'输入命令对应的序号，执行选中命令，或'
    print u'直接输入完整的命令'
    print u'这两种方法都可以通过在命令行附加相同的参数转为非交互式运行',

    # 读输入，执行
    entry_id_or_list = raw_input(u': ').strip()  # 有的 console 不能处理 raw_input 参数中的 unicode，移到 print 中
    return _exec_entry(entry_id_or_list)


def _set_syspath():
    """
    设置系统路径：当前文件的上一层目录
    """

    root_dir = os.path.abspath(os.path.realpath(__file__ + '/../../'))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)


def _set_django():
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
            DATABASE_ROUTERS=['entry.main.SQLRouter'],
            INSTALLED_APPS=INSTALLED_APPS,
            SECRET_KEY=SECRET_KEY,
            DEBUG=True
        )

        # django 设置
        django.setup()


if __name__ == "__main__":
    main()
