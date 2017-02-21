#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

# <editor-fold desc="ROOT_ANCHOR"> @formatter:off
# 由 entry.create_code.create_root 自动生成，请勿修改！
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.realpath(__file__ + '/../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# @formatter:on </editor-fold>

from libc.create_code import CreateCode


def create_blueprint():
    code0 = []
    code1 = []
    for name in ['user']:
        hash = hashlib.md5('user').hexdigest()
        code0.append('from server.blueprint.%s_controller import bp as bp%s' % (name, hash))
        code1.append('app.register_blueprint(bp%s, url_prefix=\'/%s\')' % (hash, name))
    return ['\n'.join(code0), '\n'.join(code1)]


def create_django():
    return '\n'.join([
        'from entry.django_setup import django_setup',
        '',
        'django_setup()',
    ])


def create_root():
    return '\n'.join([
        'import os',
        'import sys',
        '',
        'PROJECT_ROOT = os.path.abspath(os.path.realpath(__file__ + \'/../../\'))',
        'if PROJECT_ROOT not in sys.path:',
        '    sys.path.insert(0, PROJECT_ROOT)',
    ])


def create_sub():
    sub_modules = ['entry', 'libc', 'libs', 'model', 'server']
    return 'sub_modules = [\'' + '\', \''.join(sub_modules) + '\']'


def main():
    cc = CreateCode('server/app.py', 'BLUEPRINT_ANCHOR_IM', 'entry/create_code', 'create_blueprint')
    cc.apply_more(anchor='BLUEPRINT_ANCHOR_RE', code_seq=1)

    cc = CreateCode('entry/main.py', 'DJANGO_ANCHOR', 'entry/create_code', 'create_django')
    cc.apply_more('server/app.py', code_seq=0)

    cc = CreateCode('entry/create_code.py', 'ROOT_ANCHOR', 'entry/create_code', 'create_root')
    cc.apply_more('entry/main.py', code_seq=0)
    cc.apply_more('server/app.py', code_seq=0)

    cc = CreateCode('entry/test_all.py', 'SUB_ANCHOR', 'entry/create_code', 'create_sub')
    cc.apply_more('server/app.py', code_seq=0)
    cc.apply_more('server/app_test.py', code_seq=0)


if __name__ == '__main__':
    main()
