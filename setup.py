from setuptools import setup, find_packages

setup(
    name='pyclops',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'boto3',
        'jinja2',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        pyclops=pyclops:cli
    ''',
)
