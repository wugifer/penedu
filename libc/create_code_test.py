#!/usr/bin/python
# -*- coding: utf-8 -*-


from libc.create_code import CreateCode


# <editor-fold desc="TEST_ANCHOR1"> @formatter:off
# 由 libc.create_code_test.create_test 自动生成，请勿修改！
# hello
# @formatter:on </editor-fold>

def create_test():
    return '# hello'


def test_create_code():
    cc = CreateCode('libc/create_code_test.py', 'TEST_ANCHOR1', 'libc/create_code_test', 'create_test')
