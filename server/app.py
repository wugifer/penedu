#!/usr/bin/python
# -*- coding: utf-8 -*-


import time
from multiprocessing import Process

import pytest
from flask import Flask, render_template, redirect, request, session, url_for

from libs.config import Config

# <editor-fold desc="ROOT_ANCHOR"> @formatter:off
# 由 entry.create_code.create_root 自动生成，请勿修改！
if __name__ == '__main__':  # 避免编辑器优化破环自动化结构
    pass
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.realpath(__file__ + '/../../'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
# @formatter:on </editor-fold>

# <editor-fold desc="DJANGO_ANCHOR"> @formatter:off
# 由 entry.create_code.create_django 自动生成，请勿修改！
from entry.django_setup import django_setup

django_setup()
# @formatter:on </editor-fold>

# <editor-fold desc="BLUEPRINT_ANCHOR_IM"> @formatter:off
# 由 entry.create_code.create_blueprint 自动生成，请勿修改！
from server.blueprint.user_controller import bp as bpee11cbb19052e40b07aac0ca060c23ee
# @formatter:on </editor-fold>

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

# <editor-fold desc="SUB_ANCHOR"> @formatter:off
# 由 entry.create_code.create_sub 自动生成，请勿修改！
sub_modules = ['entry', 'libc', 'libs', 'model', 'server']
# @formatter:on </editor-fold>

def run_tests_sync():
    # entry, libc, libs, model, server
    root = [os.path.abspath(os.path.realpath('%s/../../%s' % (__file__, x))) for x in sub_modules]
    if pytest.main(root + ['--exitfirst', '--cov']) != 0:
        # 限 windows 下报警
        if os.path.join('a', 'b') == 'a\\b':
            import winsound
            winsound.PlaySound('static\\wav\\error.wav', winsound.SND_ASYNC)
            time.sleep(10)


def flask_pytest(true_app):
    inner_run = true_app.run

    def run_app(*args, **kwargs):
        # 仅在 reload 之后的进程中运行
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
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

@app.before_request
def before_request():
    if 'uid' not in session:
        if request.endpoint not in ['user.login', 'user.logout', None]:
            if not request.endpoint.endswith('static'):
                return redirect(url_for('user.login'))
                # else:
                #     try:
                #         if not request.endpoint.endswith('static'):
                #             try:
                #                 # user = DUser.get(pk=session['uid'])
                #                 # request.user = user
                #             except ObjectDoesNotExist as e:
                #                 return redirect(url_for('user.login'))
                #     except AttributeError as e:
                #         pass


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

# <editor-fold desc="BLUEPRINT_ANCHOR_RE"> @formatter:off
# 由 entry.create_code.create_blueprint 自动生成，请勿修改！
app.register_blueprint(bpee11cbb19052e40b07aac0ca060c23ee, url_prefix='/user')
# @formatter:on </editor-fold>

def main():
    Config(test=False)
    app.run(debug=True)


if __name__ == '__main__':
    main()
