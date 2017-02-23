#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
from shutil import copyfile

import pytest

from libs.config import Config


@pytest.fixture(scope="session", autouse=True)
def init_config():
    config = Config(test=True)
    base_dir = os.path.abspath('%s/../../db' % __file__)
    copyfile(os.path.join(base_dir, 'case.db'), os.path.join(base_dir, 'test.db'))
