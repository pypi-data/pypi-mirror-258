from setuptools import setup, find_packages

setup(
    name='stcp_api',
    version='0.1.0',
    author='Guilherme Borges',
    author_email='g@guilhermeborges.net',
    description='Unofficial API to retrieve STCP information for public transit buses in Porto, Portugal',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)

