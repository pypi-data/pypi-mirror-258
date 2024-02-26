from setuptools import setup, find_packages
setup(
name='pytest-in-robotframework',
version='0.0.4',
author='Petr Kus',
author_email='petrkus@email.cz',
description="Integrate PyTest with Robot Framework. Run PyTest under RF, add '@pytest_execute' decorator above Python keywords to leverage both frameworks.",
long_description=open('README.md').read(),
long_description_content_type='text/markdown',
install_requires=[
        'pytest',
        'robotframework>=6.1',
        'decorator',
        'pytest-is-running'
    ],
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.8',
)