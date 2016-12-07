# Copyright (C) 2016, see AUTHORS.md
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys

from setuptools import setup, find_packages

requires = ['slave', 'fasteners']

desc = ('An implementation of the Julabo FL RS232 interface')

setup(
    name='julabo_fl',
    version=__import__('julabo_fl').__version__,
    author='Alexander Book',
    author_email='alexander.book@frm2.tum.de',
    license = 'GNU General Public License (GPL), Version 3',
    url='https://github.com/TUM-E21-ThinFilms/Julabo-FL',
    description=desc,
    long_description=open('README.md').read(),
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
