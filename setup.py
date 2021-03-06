#!/usr/bin/env python
# This file is part sale_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from setuptools import setup
import re
import os
import io
from configparser import ConfigParser

MODULE = 'sale_jreport'
PREFIX = 'trytonzz'
MODULE2PREFIX = {
    'company_logo': 'trytonspain',
    'jasper_reports': 'trytonspain',
    'jasper_reports_options': 'trytonzz',
    'party_lang': 'trytonzz',
    'sale_discount': 'trytonspain',
    'sale_payment_type': 'trytonspain',
    }


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require

config = ConfigParser()
config.readfp(open('tryton.cfg'))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res)(\W|$)', dep):
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append(get_require_version('%s_%s' % (prefix, dep)))
requires.append(get_require_version('trytond'))

tests_require = []
series = '%s.%s' % (major_version, minor_version)
if minor_version % 2:
    branch = 'default'
else:
    branch = series
dependency_links = [
    ('hg+https://bitbucket.org/trytonspain/'
        'trytond-company_logo@%(branch)s'
        '#egg=trytonspain-company_logo-%(series)s' % {
            'branch': branch,
            'series': series,
            }),
    ('hg+https://bitbucket.org/trytonspain/'
        'trytond-jasper_reports@%(branch)s'
        '#egg=trytonspain-jasper_reports-%(series)s' % {
            'branch': branch,
            'series': series,
            }),
    ('hg+https://bitbucket.org/zikzakmedia/'
        'trytond-jasper_reports_options@%(branch)s'
        '#egg=trytonzz-jasper_reports_options-%(series)s' % {
            'branch': branch,
            'series': series,
            }),
    ('hg+https://bitbucket.org/zikzakmedia/'
        'trytond-party_lang@%(branch)s'
        '#egg=trytonzz-party_lang-%(series)s' % {
            'branch': branch,
            'series': series,
            }),
    ('hg+https://bitbucket.org/trytonspain/'
        'trytond-sale_discount@%(branch)s'
        '#egg=trytonspain-sale_discount-%(series)s' % {
            'branch': branch,
            'series': series,
            }),
    ('hg+https://bitbucket.org/trytonspain/'
        'trytond-sale_payment_type@%(branch)s'
        '#egg=trytonspain-sale_payment_type-%(series)s' % {
            'branch': branch,
            'series': series,
            }),
    ]
if minor_version % 2:
    # Add development index for testing with proteus
    dependency_links.append('https://trydevpi.tryton.org/')

setup(name='%s_%s' % (PREFIX, MODULE),
    version=version,
    description='Tryton module to Jasper Report for sale order',
    author='Zikzakmedia SL',
    author_email='zikzak@zikzakmedia.com',
    url='http://www.zikzakmedia.com',
    download_url="https://bitbucket.org/trytonspain/trytond-sale_jreport",
    package_dir={'trytond.modules.%s' % MODULE: '.'},
    packages=[
        'trytond.modules.%s' % MODULE,
        'trytond.modules.%s.tests' % MODULE,
        ],
    package_data={
        'trytond.modules.%s' % MODULE: (info.get('xml', [])
            + ['tryton.cfg', 'locale/*.po']),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'Intended Audience :: Manufacturing',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: Catalan',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    install_requires=requires,
    dependency_links=dependency_links,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    %s = trytond.modules.%s
    """ % (MODULE, MODULE),
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    use_2to3=True,
    )
