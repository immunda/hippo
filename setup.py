from setuptools import setup

setup(
    name='hippo',
    version='0.1-dev',
    py_modules=['hippo'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hippo=hippo:cli
    ''',
)