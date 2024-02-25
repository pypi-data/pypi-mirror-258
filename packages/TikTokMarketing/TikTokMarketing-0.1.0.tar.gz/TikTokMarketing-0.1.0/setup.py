from setuptools import setup, find_packages
setup(
name='TikTokMarketing',
version='0.1.0',
author='Casper Crause',
author_email='ccrause07@gmail.com',
description='A package designed to connect to the TikTok Marketing API and return data to report on.',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.10.0',
)