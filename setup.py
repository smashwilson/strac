from setuptools import setup, find_packages

setup(
    name='Strac',
    description='Trac bindings for the Store version control system.',
    author='Ash Wilson',
    author_email='smashwilson@gmail.com',

    keywords='trac plugin store smalltalk visualworks',
    url='http://azurefire.net',
    version='0.1',
    license="""
This software is provided "as is" with no warranty express or implied.
Use it at your own risk.

Permission to use or copy this software for any purpose is granted,
provided the above notices are retained on all copies.
""",
    long_description="""
        This Trac 0.10 plugin provides support for Store version control database.
    """,
    zip_safe=True,
    packages=['strac'],
    entry_points = {'trac.plugins': ['store = strac.repos']},
    install_requires=[]
)
