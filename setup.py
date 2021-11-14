from setuptools import setup
import setuptools
setup(
    name='macutil',
    version='0.1.19',
    author='Darryl lane',
    author_email='Darryllane101@gmail.com',
    url='https://github.com/Laneden-Labs/macutil',
    packages=['Package'],
    include_package_data=True,
    license='LICENSE.txt',
    description='''MAC Address brute forcing tool, used to bypass MAC based filtering''',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    scripts=['Package/macutil']
)


