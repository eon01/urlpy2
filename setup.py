from setuptools import setup


setup(
    name='urlpy',
    version='0.4',
    description='Simple URL parsing, canonicalization and equivalence.',
    long_description='''

A library with helper functions to parse URLs, and sanitize and normalize them
in pure python.

This includes support for escaping, unescaping, cleaning and sorting parameters
and query strings, and a little more sanitization.

This version is a friendly fork of the upstream url.py from Moz to keep a pure
Python version around to run on Python 2 and 3 and all OSes.
''',
    author='Aymen El Amri based on code from nexB Inc',
    url='http://github.com/eon01/urlpy2',
    py_modules=['urlpy2'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP'],
    install_requires=[
        'publicsuffix2 >= 2.20191221',
    ],
)