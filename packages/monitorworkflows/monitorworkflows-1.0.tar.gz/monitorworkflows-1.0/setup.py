#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Author:李智敏
# Wechat:anark919
# Date:2024-02-26 17:52
# Title:
from distutils.core import setup

setup(
    name="monitorworkflows",                        # 包名
    version="1.0",                            # 版本号
    descripion="工作流监控模块",              # 描述信息
    long_description="用于复杂系统架构时，减少代码量，提高系统健壮性。",  # 完整的描述信息
    author="anark919",                         # 作者
    author_email="1018803766@qq.com",          # 作者邮箱
    url="https://blog.csdn.net/qq_42874996/category_12448258.html",      # 主页
    py_modules=[							  # 希望分享模块列表
        "tools",
    ]
)
