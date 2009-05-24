from setuptools import setup, find_packages

setup(
    name='Strac',
    description='Trac bindings for the Store version control system.',
    author='Ash Wilson',
    author_email='smashwilson@gmail.com',

    keywords='trac plugin store smalltalk visualworks',
    url='http://azurefire.net',
    version='0.2',
    license="""
Copyright (c) 2009 Ashley J. Wilson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
""",
    long_description="""
        This Trac 0.11 plugin provides limited support for Store version
        control system for Smalltalk.
    """,
    zip_safe=True,
    packages=['strac'],
    entry_points = {'trac.plugins': ['store = strac.repos']},
    install_requires=[]
)
