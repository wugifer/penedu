#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import string

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

from libc.create_code import CreateCode


def create_blueprint():
    code0 = []
    code1 = []
    for name in ['user']:
        hash = hashlib.md5('user').hexdigest()
        code0.append('from server.blueprint.%s_controller import bp as bp%s' % (name, hash))
        code1.append('app.register_blueprint(bp%s, url_prefix=\'/%s\')' % (hash, name))
    return ['\n'.join(code0), '\n'.join(code1)]


def create_django():
    return '\n'.join([
        'from entry.django_setup import django_setup',
        '',
        'django_setup()',
    ])


def create_migration():
    step = {
        'm': [],
        't': []
    }

    # 扫描
    for column in os.listdir(os.path.abspath('%s/migration/' % PROJECT_ROOT)):
        # 仅跟踪卷号 = mxx, txx 结构的目录
        try:
            if len(column) != 3 or (column[0] != 'm' and column[0] != 't'):
                continue
            n_column = string.atoi(column[1:])
        except ValueError:
            continue

        for name in os.listdir(os.path.abspath('%s/migration/%s/' % (PROJECT_ROOT, column))):
            # 仅跟踪序号 = myyy_.py 结构的文件
            try:
                if name[0] != column[0] or name[4] != '_' or name[-3:] != '.py':
                    continue
                n_seq = n_column * 1000 + string.atoi(name[1:4])
            except ValueError:
                continue

            step[column[0]].append({'seq': n_seq, 'name': '%s.%s' % (column, name[:-3])})

    # 排序
    step['m'].sort(lambda x, y: cmp(x['seq'], y['seq']))
    step['t'].sort(lambda x, y: cmp(x['seq'], y['seq']))

    # 输出
    code0 = ['from migration.%(name)s import up as mu%(seq)d, down as md%(seq)d' % x for x in step['m']] + \
            [''] + \
            ['from migration.%(name)s import up as tu%(seq)d, down as td%(seq)d' % x for x in step['t']]
    code0 = '\n'.join(code0)

    code1a = ',\n'.join(['    (%(seq)d, mu%(seq)d, md%(seq)d, \'%(name)s\')' % x for x in step['m']])
    code1a = '\n'.join(['mlist = ['] + [code1a] + [']'])
    code1b = ',\n'.join(['    (%(seq)d, tu%(seq)d, td%(seq)d, \'%(name)s\')' % x for x in step['t']])
    code1b = '\n'.join(['tlist = ['] + [code1b] + [']'])

    return [code0, '\n'.join([code1a, '', code1b])]


def create_model():
    models = ['kv', 'user']
    return 'models = [\'' + '\', \''.join(models) + '\']'


def create_root():
    return '\n'.join([
        'if __name__ == \'__main__\':  # 避免编辑器优化破环自动化结构',
        '    pass',
        'import os',
        'import sys',
        '',
        'PROJECT_ROOT = os.path.abspath(os.path.realpath(__file__ + \'/../../\'))',
        'if PROJECT_ROOT not in sys.path:',
        '    sys.path.insert(0, PROJECT_ROOT)',
    ])


def create_sub():
    sub_modules = ['entry', 'libc', 'libs', 'model', 'server']
    return 'sub_modules = [\'' + '\', \''.join(sub_modules) + '\']'


def main():
    cc = CreateCode('server/app.py', 'BLUEPRINT_ANCHOR_IM', 'entry/create_code', 'create_blueprint')
    cc.apply_more(anchor='BLUEPRINT_ANCHOR_RE', code_seq=1)

    cc = CreateCode('doc/conf.py', 'DJANGO_ANCHOR', 'entry/create_code', 'create_django')
    cc.apply_more('entry/main.py', code_seq=0)
    cc.apply_more('server/app.py', code_seq=0)

    cc = CreateCode('entry/migrate.py', 'MIGRATION_ANCHOR_IM', 'entry/create_code', 'create_migration')
    cc.apply_more(anchor='MIGRATION_ANCHOR_LI', code_seq=1)

    cc = CreateCode('entry/django_setup.py', 'MODEL_ANCHOR', 'entry/create_code', 'create_model')
    cc.apply_more('entry/main.py', code_seq=0)

    cc = CreateCode('doc/conf.py', 'ROOT_ANCHOR', 'entry/create_code', 'create_root')
    cc.apply_more('entry/create_code.py', code_seq=0)
    cc.apply_more('entry/main.py', code_seq=0)
    cc.apply_more('entry/migrate.py', code_seq=0)
    cc.apply_more('server/app.py', code_seq=0)

    cc = CreateCode('entry/test_all.py', 'SUB_ANCHOR', 'entry/create_code', 'create_sub')
    cc.apply_more('server/app.py', code_seq=0)
    cc.apply_more('server/app_test.py', code_seq=0)


if __name__ == '__main__':
    main()
