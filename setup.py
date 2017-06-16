"""
flask-paginate
--------------

Simple paginate for flask (study from will_paginate).
Use bootstrap css framework, supports bootstrap2&3 and foundation
"""
from setuptools import setup

setup(
    name='flask-paginate',
    version='0.5.0',
    url='https://github.com/lixxu/flask-paginate',
    license='BSD',
    author='Lix Xu',
    author_email='xuzenglin@gmail.com',
    description='Simple paginate support for flask',
    long_description=__doc__,
    packages=['flask_paginate'],
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
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ]
)
