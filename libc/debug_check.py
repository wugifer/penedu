#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
运行时检查工具，以断言为主
"""


def accept_param(*types):
    """
    函数装饰器，检查输入参数是否为指定的类型

    Args:
        types (tuple): 期待的参数类型，指定前面若干个参数，None 表示不关心，真实参数为 None 时不检查
    """

    def decorator(func):
        def new_func(*args, **kwargs):
            # 断言参数类型完全一致
            min_len = min(len(args), len(types))
            for i in range(min_len):
                assert types[i] is None or args[i] is None or types[i] == type(args[i]), \
                    '第 %d 个参数类型为 %s, 期待 %s' % (
                        i,
                        type(args[i]).__name__,
                        types[i].__name__,
                    )

                # 执行原始函数
            return func(*args)

        # 设置 __name__
        new_func.__name__ = func.__name__
        return new_func

    return decorator
