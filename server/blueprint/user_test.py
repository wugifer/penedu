#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

import pytest
from flask import url_for

from server.app import app as flask_app


def login(client):
    client.post(url_for('user.login'), content_type='application/json',
                data='{"login": "admin", "password": "%s"}' % hashlib.md5('admin').hexdigest())


def test_login(client):
    login(client)
    assert client.get(url_for('user.login')).status_code == 200


def test_logout(client):
    assert client.get(url_for('user.logout')).status_code == 302


@pytest.fixture
def app():
    return flask_app
