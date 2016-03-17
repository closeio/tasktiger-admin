from setuptools import setup

setup(
    name='tasktiger-admin',
    version='0.2',
    url='http://github.com/closeio/tasktiger-admin',
    license='MIT',
    description='Admin for tasktiger, a Python task queue',
    platforms='any',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Framework :: Flask',
    ],
    install_requires=[
        'click',
        'flask-admin',
        'redis',
        'structlog',
        'tasktiger>=0.4',
    ],
    packages=[
        'tasktiger_admin',
    ],
    entry_points={
        'console_scripts': [
            'tasktiger-admin = tasktiger_admin.utils:run_admin',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
