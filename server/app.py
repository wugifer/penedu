#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.realpath(__file__ + '/../../')))

from flask import Flask, render_template

from multiprocessing import Process
import pytest
import time


# 自定义 flask，解决与 angularjs 的标识冲突
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='{%',
        block_end_string='%}',
        variable_start_string='{#',
        variable_end_string='#}',
        comment_start_string='<#',
        comment_end_string='#>',
    ))


################################################################################
#
# 自动测试进程，及自动测试封装


def run_tests_sync():
    # server, lib, model
    root = [
        os.path.abspath(os.path.realpath(__file__) + "/.."),
    ]
    if pytest.main(root + ['--exitfirst', '--cov']) != 0:
        # 限 windows 下报警
        if os.path.join('a', 'b') == 'a\\b':
            import winsound
            winsound.PlaySound('static\\wav\\error.wav', winsound.SND_ASYNC)
            time.sleep(10)


def flask_pytest(true_app):
    inner_run = true_app.run

    def run_app(*args, **kwargs):
        print('Running tests...')
        p = Process(target=run_tests_sync, name='background-pytest')
        p.daemon = True
        p.start()
        return inner_run(*args, **kwargs)

    true_app.run = run_app
    return true_app


################################################################################
#
# 创建 app


app = flask_pytest(CustomFlask(__name__))
app.secret_key = 'D\xe7\x82\xe2v\xc22$ha0\xa9\xc7\x97!\xfc'


################################################################################
#  首页

# @app.before_request
# def before_request():
#     if 'uid' not in session:
#         if request.endpoint not in ['user.login', 'user.logout', None]:
#             if not request.endpoint.endswith('static'):
#                 return redirect(url_for('user.login'))
#     else:
#         try:
#             if not request.endpoint.endswith('static'):
#                 try:
#                     user = DUser.get(pk=session['uid'])
#                     request.user = user
#                 except ObjectDoesNotExist as e:
#                     return redirect(url_for('user.login'))
#         except AttributeError as e:
#             pass


@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<name>.html')
def html(name):
    return render_template('%s.html' % name)


################################################################################
# 其它的 route 都在这下面



################################################################################
#
# 引入各 blueprint


if __name__ == '__main__':
    app.run(debug=True)
