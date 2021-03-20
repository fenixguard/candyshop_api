import os
import sys

from setuptools import setup

if sys.version_info < (3, 7):
    raise Exception('Candy shop requires Python 3.7 or higher.')


def strip_comments(line):
    return line.split('#', 1)[0].strip()


def reqs(*f):
    return [requirement for requirement in (strip_comments(line)
                                            for line in open(os.path.join(os.getcwd(), *f)).readlines()) if requirement]


install_requires = reqs('requirements.txt')

setup(
    name='CandyShopDeliveryApi',
    version='1.0',
    packages=[''],
    url='https://www.github.com/fenixguard/candyshop_api.git',
    license='MIT',
    author='fenixguard',
    install_requires=install_requires,
    description='Api for Candy shop Delivery'
)
