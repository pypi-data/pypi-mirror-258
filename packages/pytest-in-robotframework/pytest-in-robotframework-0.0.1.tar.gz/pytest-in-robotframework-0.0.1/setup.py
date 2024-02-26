from setuptools import setup, find_packages
setup(
name='pytest-in-robotframework',
version='0.0.1',
author='Petr Kus',
author_email='petrkus@email.cz',
description="Integrate PyTest with Robot Framework. Run PyTest under RF, add '@pytest_execute' decorator above Python keywords to leverage both frameworks.",
install_requires=[
        'pytest~=8.0.2',
        'robotframework>=6.1',
        'decorator~=5.1.1',
        'pytest-is-running~=1.5.1'
    ],
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.8',
)