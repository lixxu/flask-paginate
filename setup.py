"""
Flask-paginate
--------------

Simple paginate for Flask (study from will_paginate).
Use bootstrap css framework
"""
from setuptools import setup

setup(
    name='Flask-paginate',
    version='0.1',
    url='https://github.com/lixxu/flask-paginate',
    license='BSD',
    author='Lix Xu',
    author_email='xuzenglin@gmail.com',
    description='Simple Paginate support for Flask',
    long_description=__doc__,
    namespace_packages=['flaskext'],
    packages=['flaskext', 'flaskext.paginate'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
