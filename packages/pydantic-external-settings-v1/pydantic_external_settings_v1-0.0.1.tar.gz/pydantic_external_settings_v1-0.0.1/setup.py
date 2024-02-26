# encoding: utf-8
from setuptools import setup, find_packages

SHORT = "provide a class descriptor for pydantic to load settings from external sources." \
        "compatible with pydantic 1.x"

__version__ = "0.0.1"
__author__ = 'zhangxiaojia'
__email__ = 'zhangxiaojia002@ke.com'
readme_path = 'README.md'

setup(
    name='pydantic_external_settings_v1',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'pydantic==1.*'
    ],
    url='',
    author=__author__,
    author_email=__email__,
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    package_data={'': ['*.py', '*.pyc']},
    zip_safe=False,
    platforms='any',

    description=SHORT,
    long_description=open(readme_path, encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)
