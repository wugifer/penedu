#!/usr/bin/python
# -*- coding: utf-8 -*-


class MultiConf(object):
    """
    为属性 X 同时定义多个候选值 x1, x2, ... 通过环境变量和构造函数参数，在运行时刻动态确定 X 使用的值。
    使用方式：

    * 定义 MultiConf 的子类，比如 MyConfig
    * 在 MyConfig.__init__ 调用 MultiConf.__init__ 时传入 config, selector 参数，
      其中 config 为常量，selector 可以根据 MyConfig 的构造函数设置
    * 在程序入口第一次使用配置之前调用 MyConfig.__init__ 初始化
    * 在使用配置时调用 MultiConf.instance 单例对象

    Args:
        config (dict): 属性及候选值，每一项 key,value 包含单一配置或多重配置，多重配置通过 selector 选择其中一个配置

           * 多重配置：value 是一个元组，至少两项，且最后一项是 dict；多重配置可以嵌套

           * 单一配置：value 是其它配置

           * value 或 value 元组的任一项如果是 @xxx，表示实际值是 key2=xxx 对应的 value2

           * key 必须全部大写

        selector (dict): 多重配置选择参数，每一项 key,value 用于尝试完成多重配置选择

           * 当 key 无法匹配多重配置选择时，尝试通过 'default' 进行匹配

           * key 必须全部大写

    举例：config 中的一项为 X = (@S, {'a': 1, 'b': 2, 'c': (@DEBUG, {'True': True, 'False': False})})

       * MyConfig(config, {'S' = 'a'}) => X=1

       * MyConfig(config, {'S' = 'b'}) => X=2

       * MyConfig(config, {'S' = 'c', 'Debug' = 'True'}) => X=True

       * MyConfig(config, {'S' = 'c', 'Debug' = 'False'}) => X=False
    """

    instance = None
    """
    单例对象
    """

    def __init__(self, config, selector):
        # 转换 config 为属性
        for key in config:
            setattr(self, key, config[key])

        # 转换 selector 为属性
        for key in selector:
            setattr(self, key, selector[key])

        # 反复编译，直到无间接引用
        while self._compile():
            continue

        # 设置实例对象
        for t in self.__class__.mro():
            if 'instance' in t.__dict__:
                t.instance = self

    def create_dict(self):
        """
        通过字典形式返回全部解析后的配置

        Returns:
            dict: 解析后的配置
        """

        config = {}
        for key in dir(self):
            if key.isupper():
                config[key] = getattr(self, key)
        return config

    def dump_config(self):
        """
        在 Console 输出全部解析后的配置
        """

        for key in dir(self):
            if key.isupper():
                print key, '=', getattr(self, key)

    def _compile(self):
        """
        编译配置项
        :return: True - 任意一项配置编译发生变化，False - 均未变化
        """

        any_key_compiled = False
        for key in dir(self):
            # 只检查大写属性
            if not key.isupper():
                continue

            # 编译不同类型
            value = getattr(self, key)
            compiled = False
            if isinstance(value, str):
                compiled = self._compile_str(key, value)
            elif isinstance(value, tuple):
                compiled = self._compile_tuple(key, value)

            any_key_compiled = any_key_compiled or compiled

        return any_key_compiled

    def _compile_str(self, key, value):
        """
        编译 str 类型配置项
        :return: True - 发生变化，False - 未变化
        """

        # value 以 @ 开头，目标不再包含 @，替换
        if value and value[0] == '@':
            true_value = getattr(self, value[1:])
            if '@' in true_value:
                return False
            else:
                setattr(self, key, true_value)
                return True
        return False

    def _compile_tuple(self, key, value):
        """
        编译 tuple 类型配置项
        :return: True - 发生变化，False - 未变化
        """

        # 替换 value 中的 @xxx
        for i in range(len(value)):
            v = value[i]
            if v and isinstance(v, str) and v[0] == '@':
                true_value = getattr(self, v[1:])
                if not isinstance(true_value, str) or '@' in true_value:
                    continue
                else:
                    setattr(self, key, value[0:i] + (true_value,) + value[i + 1:])
                    return True

        # 选择器与被选择器，选择结果
        selector = value[:-1]
        selecting = value[-1]
        selected = {}

        if not isinstance(selecting, dict):
            return False

        for name in selector:
            if not isinstance(name, str) or (name and name[0] == '@'):
                return False

            # name 是 string, selecting 是 dict，返回 dict[name] or dict['default'] or None
            if name in selecting:
                selected[name] = selecting[name]
            elif 'default' in selecting:
                selected[name] = selecting['default']
            else:
                return False

        # 用 selected 替换原始值，其中 selected 仅有一个元素时，只保留结果，附加 key_K 属性
        if len(selected) == 1:
            setattr(self, key, selected.values()[0])
            setattr(self, '%s_K' % key, selected.keys()[0])
        else:
            setattr(self, key, selected)
        return True
