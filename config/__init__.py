#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       JackyPJB
    @   date    :       2019/6/1 0001 下午 11:24
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""

__author__ = 'Max_Pengjb'
import os


def load_config():
    """Load config."""
    # 获取环境变量，判断当前是处于什么模式，开发模式还是生产模式
    # 我这里定义的是三种 开发 DEV  产品 PRO 测试 TEST，详见config.__init__.py
    mode = os.environ.get("MODE")

    try:
        if mode == 'PRO':
            from .production import ProductionConfig
            return ProductionConfig
        elif mode == 'TEST':
            from .testing import TestingConfig
            return TestingConfig
        else:
            from .development import DevelopmentConfig
            return DevelopmentConfig
    except ImportError:
        from .default import Config
        return Config
