# setup.py
from setuptools import setup, find_packages

setup(
    name='netbox-ssl-certificates',
    version='0.1',
    description='NetBox plugin for tracking SSL certificates',
    author='Cesar Villanueva',
    author_email='ceo@sciverint.com',
    url='https://github.com/sciverint/netbox-ssl-certificates/netbox-ssl-certificates/',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'netbox>=3.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
