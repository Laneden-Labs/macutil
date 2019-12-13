from setuptools import setup

setup(
    name='macutil',
    version='0.1.2',
    author='Darryl lane',
    author_email='DarrylLane101@gmail.com',
    url='https://github.com/ignoto101/macutil',
    packages=['Macutil'],
    include_package_data=True,
    license='LICENSE.txt',
    description='''MAC Address brute forcing tool, used to bypass MAC based filtering''',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    scripts=['Macutil/macutil'],
)

