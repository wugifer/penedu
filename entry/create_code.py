#!/usr/bin/python
# -*- coding: utf-8 -*-


# ROOT_ANCHOR
# 由 main.create_root_path 自动生成，请勿修改！
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.realpath(__file__ + '/../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# ROOT_ANCHOR

from lib.create_code import CreateCode


def main():
    cc = CreateCode('create_code.py', 'ROOT_ANCHOR', 'main', 'create_root_path')
    cc.apply_more('main.py', 'ROOT_ANCHOR', code_seq=0)

    cc = CreateCode('main.py', 'DJANGO_ANCHOR', 'django_setup', 'create_django_setup')


if __name__ == '__main__':
    main()
