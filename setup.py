"""
flask-paginate
--------------

Simple paginate for flask (study from will_paginate).
Use bootstrap css framework, supports bootstrap2&3 and foundation
"""
import io
import os.path
from setuptools import setup

version = ""
work_dir = os.path.dirname(os.path.abspath(__file__))
fp = os.path.join(work_dir, "flask_paginate/__init__.py")
with io.open(fp, encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__ = "):
            version = line.split("=")[-1].strip().replace("'", "")
            break

setup(
    name="flask-paginate",
    version=version.replace('"', ""),
    url="https://github.com/lixxu/flask-paginate",
    license="BSD-3-Clause",
    author="Lix Xu",
    author_email="xuzenglin@gmail.com",
    description="Simple paginate support for flask",
    long_description=__doc__,
    packages=["flask_paginate"],
    zip_safe=False,
    platforms="any",
    install_requires=["Flask"],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
