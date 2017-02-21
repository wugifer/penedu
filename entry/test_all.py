#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

import pytest
from libs.config import Config

# <editor-fold desc="SUB_ANCHOR"> @formatter:off
# 由 entry.create_code.create_sub 自动生成，请勿修改！
sub_modules = ['entry', 'libc', 'libs', 'model', 'server']
# @formatter:on </editor-fold>


def main():
    Config(True)
    root = [os.path.abspath(os.path.realpath('%s/../../%s' % (__file__, x))) for x in sub_modules]
    pytest.main(root + ['--exitfirst', '--cov', '--cov-report', 'html'])

if __name__ == '__main__':
    main()