#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from libc.multiconf import MultiConf


class Config(MultiConf):
    """
    配置项，通过环境变量 SIEVE_SELECTOR 进行运行环境选择，区分不同的开发机、运行服务器等，未设置为 DEV

    Args:
        test (bool): 单元测试环境
        case (bool)：单元测试环境，用于准备测试用例，隐含 test = True
    """

    def __init__(self, test=False, case=False):
        # 环境选择
        assert isinstance(test, bool) and isinstance(case, bool)
        selector = os.getenv('SIEVE_SELECTOR', 'DEV')
        if case:
            test = True

        config = {
            ################################################################################
            #  app 相关

            # 服务器监听地址
            'APP_ADDR': '0.0.0.0',

            # 服务器启用 debug 模式
            'APP_DEBUG': True,

            # 服务器监听端口
            'APP_PORT': 5081,

            # 后台代理程序监听端口
            'APP_PROXY_PORT': 20659,

            # 后台任务程序监听端口
            'APP_TASK_PORT': 23154,

            ################################################################################
            # es 相关

            # ES 服务器地址
            'ES_ADDR': ('@S', {
                'default': self._get_docker('ES_PORT')[0],
                'EXAMPLE': '127.0.0.2',
                'WG': '127.0.0.1',
                'MYC': '127.0.0.1'
            }),

            # ES 服务器端口
            'ES_PORT': 9286,

            # ES 前缀
            'ES_PREFIX': ('@TEST', {'default': 'sieve', 'True': 'test'}),

            ################################################################################
            # redis 相关

            # redis 服务器地址
            'RS_ADDR': ('@S', {
                'default': self._get_docker('REDIS_PORT')[0],
                'EXAMPLE': '127.0.0.2',
                'WG': '127.0.0.1',
                "MYC": '127.0.0.1'
            }),

            # ES 服务器端口
            'RS_PORT': 6379,

            ################################################################################
            # upload 相关

            # SQL 服务器地址
            'SQL_ADDR': ('@S', {
                'default': self._get_docker('MYSQL_PORT')[0],
                'EXAMPLE': '127.0.0.2',
                'WG': '127.0.0.1',
                'MYC': '127.0.0.1'
            }),

            # SQL 数据库
            'SQL_DB': ('@TEST', {'default': 'sieve', 'True': 'test'}),

            ################################################################################
            # upload 相关

            # 上传服务器列表
            'UPLOAD_ADDRS': {'S1': '10.208.36.199', 'S2': '10.208.36.200', 'S3': '10.208.36.229'},

            # 上传服务器端口
            'UPLOAD_PORT': 5082
        }

        super(Config, self).__init__(config, {'S': selector, 'TEST': test.__str__(), 'CASE': case.__str__()})

    def _get_docker(self, key):
        # tcp://172.17.0.4:3306，返回 ['127.0.0.1', '1234']
        value = os.getenv(key, 'tcp://127.0.0.1:1234')
        value = value.split(':')
        return [value[1][2:], value[2]]
