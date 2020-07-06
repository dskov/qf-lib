#     Copyright 2016-present CERN – European Organization for Nuclear Research
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='qf-lib',
    version='1.0.0',
    author='Jacek Witkowski, Marcin Borratynski, Thomas Ruxton, Dominik Picheta, Olga Kalinowska, Karolina Cynk',
    author_email='qf-lib@cern.ch',
    description='Quantitative Finance Library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://quarkfin.github.io/qf-lib/',
    packages=find_packages(),
    provides=[
        'qf_lib'
    ],
    include_package_data=True,
    install_requires=[
        'numpy==1.15.4',
        'scipy==1.1.0',
        'dic==1.5.2b1',
        'matplotlib==2.2.0',
        'openpyxl==2.5.9',
        'pandas==0.23.4',
        'scikit-learn==0.20.0',
        'xlrd==1.1.0',
        'emails==0.5.15',
        'Jinja2==2.10.1',
        'WeasyPrint==44',
        'seaborn==0.9.0',
        'statsmodels==0.9.0',
        'arch==4.6.0',
        'quandl==3.4.4',
        'beautifulsoup4==4.6.3',
        'mockito==1.1.1',
        'xarray==0.11.0',
        'cvxopt==1.2.2',
		'Pillow==5.4.1',
		'patsy==0.5.1'
		],
    keywords='quantitative finance backtester',
    project_urls={
        'Source': 'https://github.com/quarkfin/qf-lib'
    },
    python_requires='>=3.6.0'
)
