from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='SimpleMLP',
    version='1.0.1',
    description='test',
    author='Freeze',
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type='text/plain',
    url='https://github.com/TheFreezeBee/SimpleMLP',
    extras_require = {'dev' : ["pytest>=7.0", "twine>=4.0.2"]},
    python_requires =">=3.8",
)