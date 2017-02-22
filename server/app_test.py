#!/usr/bin/python
# -*- coding: utf-8 -*-

import importlib
import os

import pytest
from dependenpy.utils import MatrixBuilder
from flask import url_for

from server.app import app as flask_app
from server.blueprint.user_test import login


# 未登录
def test_not_login(client):
    assert client.get(url_for('index')).status_code == 302


# 用户、密码错误
def test_login_error(client):
    response = client.post(url_for('user.login'), content_type='application/json',
                           data='{"login": "xxx", "password": "yyy"}')
    assert response.status_code == 200 and 'login' in response.json and response.json['login'] == 'fail'


# 密码正确
def test_login_ok(client):
    login(client)
    assert client.get(url_for('index')).status_code == 200


# def test_index(client):
#     login(client)
#     response = client.get(url_for('index'))
#     assert response.status_code == 200
#     assert 'main-sidebar' in response.data


# def test_html(client):
#     login(client)
#     assert client.get(url_for('html', name='menu')).status_code == 200


# def test_api():
#     collect_and_match_api(flask_app)

# <editor-fold desc="SUB_ANCHOR"> @formatter:off
# 由 entry.create_code.create_sub 自动生成，请勿修改！
sub_modules = ['entry', 'libc', 'libs', 'model', 'server']
# @formatter:on </editor-fold>

def test_anything_and_nothing():
    # 遍历文件夹
    root_dir = os.path.abspath(os.path.realpath(__file__) + "/../../")
    root_dir_len = len(root_dir)
    folder_list = [os.path.abspath('%s/%s' % (root_dir, sub)) for sub in sub_modules]

    while folder_list:
        folder = folder_list.pop()
        for fname in os.listdir(folder):
            fullname = os.path.join(folder, fname)
            if os.path.isfile(fullname):
                if fullname.endswith('.py'):
                    # 单纯 import，使文件名出现在 coverage 列表中，并验证文件最外层语法无误
                    module_name = fullname[root_dir_len + 1:-3].replace('\\', '.')
                    importlib.import_module(module_name)
            else:
                folder_list.append(fullname)


myapps = [
    # APP_ANCHOR
    # 由 create_code.create_app 自动生成，请勿修改！
    'build',
    'doc',
    'libs',
    'main',
    'migration',
    'misc',
    'models',
    'server',
    'task'
    # APP_ANCHOR
]


def test_imports():
    dm = MatrixBuilder(myapps)

    dm.build()

    # 过滤掉测试用例，留下 imports 部分
    imports = [x for x in dm.imports if not x['source_name'].endswith('_test')]
    imports = reduce(lambda x, y: x + y['imports'], imports, [])
    print imports
    for imp in imports:
        for target in imp['import']:
            assert target != '*' and not target.startswith('_')


@pytest.fixture
def app():
    return flask_app
