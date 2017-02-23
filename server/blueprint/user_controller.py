#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, render_template, session, redirect, url_for

from model.user.models import User

bp = Blueprint('user', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录页面。GET - 显示登录页面；POST - 发送 json 请求，验证登录信息

    json 输入：{"login": "xxx", "hash": "xxx"}，其中 hash 是经过计算的密码验证信息，参考 :meth:`model.user.models.User.verify`。

    json 输出：{"login": "xxx"，"msg"："yyy"}，其中 xxx 是 ok、fail 之一，"msg" 在 fail 时有效
    """

    # GET 页面
    if request.method == 'GET':
        return render_template('user/login.html')

    # 获取 json 参数，此处缺少合法性验证
    j = request.get_json()
    user = User.objects.filter(login=j['login'])

    # 用户存在
    if user.count() == 1:
        user = user[0]

        # 密码验证成功
        if user.verify(j['hash'], timeout=5):
            session['login'] = user.login
            session['uid'] = user.id
            return '{"login": "ok"}'
        else:
            return '{"login": "fail", "msg": "verify fail"}'

    # 用户不存在或不唯一
    return '{"login": "fail", "msg": "user %s fail"}' % j['login']


@bp.route('/logout')
def logout():
    """
    登出，重定向到登录页面
    """

    session.clear()
    return redirect(url_for('user.login'))
