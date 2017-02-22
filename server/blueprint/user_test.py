#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import hashlib

import pytest
from flask import url_for

from server.app import app as flask_app


def login(client):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    client.post(url_for('user.login'), content_type='application/json',
                data='{"login": "test", "hash": "%s"}' % hashlib.md5(
                    now + hashlib.md5('123456').hexdigest()).hexdigest())


def test_login(client):
    login(client)
    assert client.get(url_for('user.login')).status_code == 200


def test_logout(client):
    assert client.get(url_for('user.logout')).status_code == 302


@pytest.fixture
def app():
    return flask_app
