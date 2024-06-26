import re

from setuptools import setup

VERSION_FILE = "tasktiger_admin/__init__.py"
with open(VERSION_FILE, encoding="utf8") as fd:
    version = re.search(r'__version__ = ([\'"])(.*?)\1', fd.read()).group(2)

with open("README.rst", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="tasktiger-admin",
    version=version,
    url="http://github.com/closeio/tasktiger-admin",
    license="MIT",
    description="Admin for tasktiger, a Python task queue",
    long_description=long_description,
    platforms="any",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Flask",
    ],
    install_requires=[
        "click",
        "flask-admin",
        "redis>=2,<5",
        "structlog",
        "tasktiger>=0.19",
    ],
    packages=["tasktiger_admin"],
    entry_points={
        "console_scripts": [
            "tasktiger-admin = tasktiger_admin.utils:run_admin"
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
