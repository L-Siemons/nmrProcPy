from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='nmrProcPy',
    version='0.1.0',
    author='L. Siemons',
    author_email='lucas.siemons@googlemail.com',
    packages=find_packages(),
    #package_data={'just_another_Bfactor': ['resources/*dat']},
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    
    #should include a license for public things
    #license='LICENSE.txt',
    
    description='Module for converting nmr measurements from a spectrum to useful values',
    long_description=open('README.txt').read(),
    install_requires=['numpy'],
    )
