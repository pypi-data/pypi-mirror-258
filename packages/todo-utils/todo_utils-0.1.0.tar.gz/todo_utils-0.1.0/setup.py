#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "PyYAML",
    "Rich",
    "pydantic",
]

test_requirements = [ ]

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Convenient tool for scanning entire codebase to find TODO and FIXME comments and then updating the TODO.md.",
    entry_points={
        'console_scripts': [
            'scan-codebase=todo_utils.scan_codebase:main',
            'update-todo-md=todo_utils.update_todo_md:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='todo_utils',
    name='todo_utils',
    packages=find_packages(include=['todo_utils', 'todo_utils.*']),
    package_data={"todo_utils": ["conf/config.yaml"]},
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/todo-utils',
    version='0.1.0',
    zip_safe=False,
)
