# This file is part of django-infinite-scroll
#
#    django-infinite-scroll is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    django-infinite-scroll is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with django-infinite-scroll. If not, see <http://www.gnu.org/licenses/>.

import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-infinite-scroll',
    version='0.1.6',
    packages=find_packages(),
    include_package_data=True,
    license='GNU License',
    description='Adds infinite scroll to any page',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/gsteixeira',
    author='Gustavo Selbach Teixeira',
    author_email='gsteixei@gmail.com',
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        ],
    install_requires=[
        'Django>=2.2.0',
        ],
    package_data={
        },
)
