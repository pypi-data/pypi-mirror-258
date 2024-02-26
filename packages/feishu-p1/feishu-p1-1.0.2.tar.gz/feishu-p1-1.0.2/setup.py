# encoding: utf-8
"""
@author: liyao
@contact: liyao2598330@126.com
@software: pycharm
@time: 2020/6/12 1:39 下午
@desc:
"""

import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="feishu-p1",
    version="1.0.2",
    author="tutu",
    author_email="tutu@gmail.com",
    description="Feishu Third-party Libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tutan123/feishu-p1",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",

    ],
    install_requires=[
        'urllib3',
        'requests'
    ],
    python_requires='>=2.7',
)
