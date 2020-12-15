
from setuptools import setup, find_packages
from rapidodeveloper.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='rapidodeveloper',
    version=VERSION,
    description='Tool for Easy Blender Addon Development',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Romeo Disca',
    author_email='romeo.disca@gmail.com',
    url='https://github.com/i-think-rapido/blender-addon-rapidodeveloper',
    license='GPL',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'rapidodeveloper': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        rapidodeveloper = rapidodeveloper.main:main
    """,
)
