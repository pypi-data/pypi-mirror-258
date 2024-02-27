#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='hi_spike',
    version='0.0.83',
    author='deng1fan',
    author_email='dengyifan@iie.ac.cn',
    url='https://github.com/deng1fan',
    description=u'工具包，包含 Redis 安装、基于 Redis 的GPU 任务队列管理等功能',
    long_description=open("README.md", "r", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'nvitop',
        'redis',
        'rich',
        'psutil',
        'jsonlines',
        'setproctitle',
        'traceback'
    ],
    exclude=["*.tests", "*.tests.*", "tests"],
    include_package_data=True,
    python_requires='>=3.6',
    keywords=['gpu', 'queuer', 'redis'],
    entry_points = {
        'console_scripts' : [
            # 这一行是安装到命令行运行的关键
            'spike = spike.cmd_utils:main',
        ]
    }
)
