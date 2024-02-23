# -*- coding: utf-8 -*-
"""
Created on Fri Aug 3 13:30:11 2018

@author: danielgodinez
"""
from setuptools import setup, find_packages, Extension

setup(
    name="MicroLIA",
    version="2.7.0",
    author="Daniel Godines",
    author_email="danielgodinez123@gmail.com",
    description="Machine learning classifier for microlensing",
    license='GPL-3.0',
    url = "https://github.com/Professor-G/MicroLIA",
    classifiers=[
		'Development Status :: 5 - Production/Stable',
		'Intended Audience :: Developers',
		'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3',	   
],
    packages=find_packages('.'),
    install_requires = ['numpy','scikit-learn', 'scikit-optimize', 'astropy','scipy','peakutils',
        'progress', 'matplotlib', 'optuna', 'boruta', 'BorutaShap', 'xgboost', 'scikit-plot',
        'pandas', 'dill', 'opencv-python', 'gatspy', 'astroML'],
    python_requires='>=3.7,<4',
    include_package_data=True,
    test_suite="nose.collector",
    package_data={
        'MicroLIA': ['data/Miras_vo.xml', 'data/Sesar2010/*', 'test/test_model_xgb/MicroLIA_ensemble_model/*', 'test/test_classifier.py', 
            'test/test_features.py', 'test/MicroLIA_Training_Set_OGLE_IV.csv', 'test/test_ogle_lc.dat']
    },
)
