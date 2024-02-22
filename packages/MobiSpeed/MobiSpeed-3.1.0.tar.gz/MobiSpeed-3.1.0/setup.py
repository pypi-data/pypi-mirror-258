# setup.py
from setuptools import setup, find_packages

setup(
    name='MobiSpeed',
    version='3.1.0',
    packages=find_packages(),
    package_data={'MobiSpeed': ['MobiSpeed/*']},
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'MobiSpeed=MobiSpeed.module:main',
        ],
    },
    author='Aji permana',
    license='MIT',
    platforms=['Linux'],
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    author_email='admin@MobiSpeed.net',
    description='MobiSpeed VPN autoinstall script ssh-vpn installation module with layered encryption.',
)

