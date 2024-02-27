from setuptools import setup, find_packages

setup(
    name='ppai-dev',
    version='0.1',
    packages=find_packages(),
    install_requires=['requests', 'typing'],
    url='https://github.com/freihandlabor/peakprivacyai-python-dev',
    license='MIT',
    author='PeakPrivacy',
    author_email='ppai-python@pp.com',
    description='The library provides convenient access to the PeakPrivacy AI REST API',
)
