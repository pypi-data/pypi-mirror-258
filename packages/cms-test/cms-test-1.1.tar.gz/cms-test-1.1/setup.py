from setuptools import setup, find_packages

setup(
    name='cms-test',
    version='1.1',
    author='HCMP DE',
    author_email='Rishabh2.Mehta@ril.com',
    description='CMS Helper library',
    url='https://github.com/test/cms',
    packages=find_packages(),
    install_requires=[
        'requests',
        'loguru',
        'pycryptodome',
        'setuptools'
    ]
)