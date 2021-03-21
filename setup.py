from setuptools import setup
from os import path


def get_long_description():
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name='dark-keeper',
    version='0.3.1',
    packages=['dark_keeper'],
    url='https://github.com/itcrab/dark-keeper',
    license='MIT License',
    author='Arcady Usov',
    author_email='itcrab@gmail.com',
    maintainer='Arcady Usov',
    maintainer_email='itcrab@gmail.com',
    description='Dark Keeper is open source simple web-parser for podcast-sites',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    install_requires=[
        'cssselect==1.1.0',
        'lxml==4.6.2',
        'pymongo==3.11.3',
        'requests==2.25.1',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
