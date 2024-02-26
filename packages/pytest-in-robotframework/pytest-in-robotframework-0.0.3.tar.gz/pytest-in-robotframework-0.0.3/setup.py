from setuptools import setup, find_packages
setup(
name='pytest-in-robotframework',
version='0.0.3',
author='Petr Kus',
author_email='petrkus@email.cz',
description="Integrate PyTest with Robot Framework. Run PyTest under RF, add '@pytest_execute' decorator above Python keywords to leverage both frameworks.",
long_description=
"""
This feature enables the running of PyTests within the Robot Framework, allowing users to leverage the advantages of both frameworks.

To achieve this integration, simply add the decorator '@pytest_execute' above all the PyTest fixtures within your Python tests/keywords in Python libraries.

At present, this code serves as a proof of concept. It is hardcoded to use the TestExperiment.py file (your library must be named TestExperiment) and the TestExperiment class. 
PyTest's console logs are captured as informational messages in Robot Framework logs. If any test in PyTest fails, the entire keyword in Robot Framework fails.

Generalization of this code will be made in the near future, along with enhanced logging from PyTest.
""",
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