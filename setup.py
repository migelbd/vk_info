import os, sys
from app import __version__
from setuptools import setup, find_packages

requirements = [
    'certifi==2021.5.30',
    'charset-normalizer==2.0.4',
    'click==8.0.1',
    'colorama==0.4.4',
    'commonmark==0.9.1',
    'idna==3.2',
    'profig==0.5.1',
    'prompt-toolkit==3.0.20',
    'Pygments==2.10.0',
    'questionary==1.10.0',
    'requests==2.26.0',
    'rich==10.9.0',
    'six==1.16.0',
    'urllib3==1.26.6',
    'vk-api==11.9.4',
    'wcwidth==0.2.5',
]

if sys.version.startswith("2.6"):
    requirements.append("argparse==1.3.0")

setup(
    name="VkInfo CLI Tool",
    version=".".join(map(str, __version__)),
    description="A command-line utility",
    url='https://github.com/migelbd/vk_info',
    license='MIT',
    author='migelbd',
    author_email='migel.bd@gmail.com',
    packages=['redmine'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires=requirements,
    tests_require=[],
    entry_points={
        'console_scripts': [
            'vkifno = app.core:cli',
        ]
    }
)
