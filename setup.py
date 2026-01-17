'''
Function:
    Implementation of Setup
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu/videodl
'''
import videodl
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''setup'''
setup(
    name=videodl.__title__,
    version=videodl.__version__,
    description=videodl.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=videodl.__author__,
    url=videodl.__url__,
    author_email=videodl.__email__,
    license=videodl.__license__,
    include_package_data=True,
    packages=find_packages(),
    package_data={"videodl": [
        "modules/cdm/*.wvd", "modules/js/youtube/*.js", "modules/js/xmflv/*.js", "modules/js/xmflv/xiami_token.wasm", "modules/js/tencent/*.js", "modules/js/tencent/ckey.wasm",
    ]},
    entry_points={'console_scripts': ['videodl = videodl.videodl:VideoClientCMD']},
    install_requires=[lab.strip('\n') for lab in list(open('requirements.txt', 'r').readlines())],
    zip_safe=True,
)