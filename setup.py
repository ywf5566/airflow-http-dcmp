from __future__ import print_function
from setuptools import setup, find_packages


setup(
    name="kd_airflow_dag",
    version='1.0.0',
    author="WenFeng.yu",
    author_email="",
    description="通过Http请求的方式往不同服务器上的airflow服务进行dag任务的管理操作",
    license="MIT",
    url="",
    packages=find_packages(exclude=['tests', 'test*']),
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Chinese',
        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Topic :: Quantum',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        # 依赖安装顺序不能变
        'twine>=3.2.0',
        'requests',
        'robobrowser',
        'paramiko',
        'croniter',
        'sqlalchemy>=1.3.20'
    ],
    zip_safe=True,
)
