from setuptools import setup, find_packages
setup(
name='cnv_vcf2json',
version='1.0.0',
author='Khaled Jumah',
author_email='khalled.joomah@yahoo.com',
description='Converts the structural variants VCF file into JSON file',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)
