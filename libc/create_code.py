#!/usr/bin/python
# -*- coding: utf-8 -*-

import importlib
import os

from libc.debug_check import accept_param


class CreateCode:
    """
    使用自动生成的代码替换指定文件中的代码。执行时会判断目标代码片段是否改变，仅当目标代码变化后才替换。

    Args:
        target (str): 自动化代码目标文件，相对于项目根路径，不能以 '/' 开头
        anchor (str): 界定符，自动化代码位于第一个 anchor 和第二个 anchor 之间，
                      anchor 可以在任意位置，且不需要独占一行，自动化代码与两个 anchor 均不在同一行，
                      自动化代码的第一行提示与第一个 anchor 对齐
        source (str): 产生自动化代码的文件，相对于项目根路径，不能以 '/' 开头，不含后缀名
        func   (str): 产生自动化代码的函数，返回值为目标代码/目标代码列表，其中第一段被本次调用使用，
                      其余的被后续的 apply_more() 使用
        args (tutle): 可变长度参数，传递给 func
    """

    @accept_param(None, str, str, str)
    def __init__(self, target, anchor, source, func, *args):
        # 记录参数
        self.target = target
        self.anchor = anchor

        # 获得调用者的绝对路径
        self._get_base_path()

        # 生成新的代码
        self._create_code(source, func, *args)

        # 应用
        self.apply_more(target, anchor, 0)

    def apply_more(self, target=None, anchor=None, code_seq=0):
        """
        使用已生成的代码替换指定文件中的代码。执行时会判断目标代码片段是否改变，仅当目标代码变化后才替换。

        Args:
            target (str): 自动化代码目标文件，None 表示使用上一次 apply_more() 或 __init__() 时的参数
            anchor (str): 界定符，None 表示使用上一次 apply_more() 或 __init__() 时的参数
            code_seq (int): 从已生成的多段目标代码中选择一段，code_seq 为序号
        """

        # 更新参数
        self.target = target or self.target
        self.anchor = anchor or self.anchor

        # 加载目标文件，获得文件内容及定位
        if not self._get_target(self.target, self.anchor):
            return

        # 如果代码有更新，修改目标文件
        if self.codes and (' ' * self.tip_start + self.codes[code_seq]) != self.text[self.start:self.end]:
            self._set_target(code_seq)

    def _create_code(self, source, func, *args):
        """
        产生代码
        """

        # 加载
        filename = source.replace('/', '.').replace('\\', '.')
        imodule = importlib.import_module(filename)
        ifunc = getattr(imodule, func)

        # 执行
        codes = ifunc(*args)
        if type(codes) == str:
            codes = [codes]

        # 执行，tip_start 此时还未确定，# 之前的空格暂不输出
        self.codes = ['# 由 %s.%s 自动生成，请勿修改！\n%s\n' % (
            filename,
            func,
            code
        ) for code in codes]

    def _get_base_path(self):
        """
        获得项目根路径
        """

        self.base_path = os.path.abspath(os.path.realpath('%s/../../' % __file__))

    @accept_param(None, str, str)
    def _get_target(self, target, anchor):
        """
        获得 target 文件内容及 anchor 之间区域的 [start, end) 位置
        """

        # 读
        path = os.path.realpath('%s/%s' % (self.base_path, target))
        ifile = file(path, 'rb')
        self.text = ifile.readlines()
        ifile.close()

        # 定位 start
        start_line = None
        for line in range(len(self.text)):
            self.start = self.text[line].find(anchor)
            if self.start >= 0:
                self.tip_start = max(0, self.start - 2)
                self.start = sum([len(self.text[x]) for x in range(line + 1)])
                start_line = line + 1
                break

        if not start_line:
            return False

        # 定位 end
        for line in range(start_line, len(self.text)):
            self.end = self.text[line].find('</editor-fold>')
            if self.end >= 0:
                self.end = sum([len(self.text[x]) for x in range(line)])
                break

        if not self.end or self.end < 0:
            return False

        # 合并诸行
        self.text = ''.join(self.text)
        return True

    @accept_param(None, int)
    def _set_target(self, code_seq):
        """
        设置代码
        """

        # 写
        filename = os.path.abspath('%s/%s' % (self.base_path, self.target))
        ofile = file(filename, 'wb')
        ofile.write('%s%s%s%s' % (
            self.text[:self.start],
            '',  # ' ' * self.tip_start,
            self.codes[code_seq],
            self.text[self.end:]
        ))
        ofile.close()


# <editor-fold desc="ANCHOR1"> @formatter:off
# 由 libc.create_code._create_anything 自动生成，请勿修改！
# hi，修改自身也是可以的哈
# @formatter:on </editor-fold>

# <editor-fold desc="ANCHOR2"> @formatter:off
# 由 libc.create_code._create_anything 自动生成，请勿修改！
# hi，修改自身也是可以的哈...2
# @formatter:on </editor-fold>

def _create_anything(text):
    return [text, text + '...2']


if __name__ == '__main__':
    cc = CreateCode('libc/create_code.py', 'ANCHOR1', 'libc/create_code', '_create_anything', '# hi，修改自身也是可以的哈')
    cc.apply_more(anchor='ANCHOR2', code_seq=1)
