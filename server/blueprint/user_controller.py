#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request, render_template, session, redirect, url_for

bp = Blueprint('user', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    GET: 登录页面
    POST: 包含 login, password 的 json 请求
    :return: {'login': 'ok'} or {'error': ''}
    """
    if request.method == 'GET':
        return render_template('user/login.html')

    session['uid'] = 'hello'
    return '{"error":""}'
    # data = login_validate(request, session)
    # if DUser.exist(**data):
    #     session['login'] = data['login']
    #
    #     # save user's id into session
    #     user = DUser.get(login=data['login'])
    #     session['uid'] = user.id
    #
    #     RedisSession.get(session, 'key-is-not-used')
    #     return jsonify({'login': 'ok'})
    # else:
    #     return jsonify({'error': ''})


@bp.route('/logout')
def logout():
    if request.args.get('clean') == '1':
        RedisSession.clean(session)
    session.clear()
    return redirect(url_for('user.login'))
