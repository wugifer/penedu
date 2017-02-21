#!/usr/bin/python
# -*- coding: utf-8 -*-

import string
import traceback

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

from libs.config import Config
from model.kv.models import Kv

# <editor-fold desc="MIGRATION_ANCHOR_IM"> @formatter:off
# 由 entry.create_code.create_migration 自动生成，请勿修改！
from migration.m00.m001_default_user import up as up1, down as down1
# @formatter:on </editor-fold>


class Migration():
    def __init__(self):
        try:
            self.last = Kv.objects.get(group='system', key='migration')
        except Kv.DoesNotExist:
            self.last = Kv.objects.create(group='system', key='migration', n=0)

    def run(self, max_step=99999, down=0):
        """
        执行数据迁移
        :return:
        """

        last_migration = self.last.n
        print 'last migration step ==> %d' % last_migration

        # 回退
        if (down != 0):
            min_step = down if down > 0 else last_migration + down
            for step in reversed(step_list):
                if step[0] > min_step and step[0] <= last_migration:
                    if not self.run_updown(step, step[2]):
                        break
                    # 记录
                    self.set_migration(step[0] - 1)
            return

        # 前进
        for step in step_list:
            if step[0] > last_migration and step[0] <= max_step:
                if not self.run_updown(step, step[1]):
                    break
                # 记录
                self.set_migration(step[0])

    def run_updown(self, step, up_or_down):
        try:
            up_or_down()
            print 'run %s ... ok!' % step[3]
            return True
        except:
            print 'run %s ... fail!' % step[3]
            lines = traceback.format_exc().splitlines()
            lines = [lines[i] for i in range(len(lines)) if i % 2 == 1 or i == len(lines) - 2]
            print u'  %s\n%s' % (lines[-1], '\n'.join(lines[:-1]))
            return False

    def set_migration(self, step):
        self.last.n = step
        self.last.save()


# <editor-fold desc="MIGRATION_ANCHOR_LI"> @formatter:off
# 由 entry.create_code.create_migration 自动生成，请勿修改！
step_list = [
    (1, up1, down1, 'm00.m001_default_user')
]
# @formatter:on </editor-fold>

def main(*args):
    for case in [True, False]:
        # 设置不同的环境
        config = Config(case=case)

        print
        print 'case=', case

        # down = 0
        # down = -n, 回退 n 步，限开发过程中不同分支间的版本迁移，慎用
        # down =  n, 回退到第 n 步（不含），限开发过程中不同分支间的版本迁移，慎用

        # max_step = nn，限调试用，更新到 nn (含）则截止，不再继续更新

        assert (len(args) == 2)
        Migration().run(max_step=string.atoi(args[0]), down=string.atoi(args[1]))


if __name__ == '__main__':
    main('99999', '0')
