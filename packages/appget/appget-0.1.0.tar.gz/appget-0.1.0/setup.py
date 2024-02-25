#!/usr/bin/python3

import os
import setuptools

setuptools.setup(
    name='appget',
    version='0.1.0',
    keywords='appget',
    description='A package management tool.',
    license='MIT',
    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),
    author='lonelypale',  # 替换为你的pypi官网账户名
    author_email='lonelypale@126.com',  # 替换为你pypi账户名绑定的邮箱
    url='https://github.com/LonelyPale/appget',  # 这个地方为github项目地址，貌似非必须
    packages=setuptools.find_packages(),
    # install_requires=['fire'],
    python_requires='>=3',
    # 如果需要支持脚本方法运行，可以配置入口点
    # entry_points={
    #     'console_scripts': [
    #         'lone = lonely.__main__:main'
    #     ]
    # },
)
