from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
  name='diapasons',
  version='0.0.2',
  author='a.sabirzianov',
  author_email='albertuno@mail.com',
  description='simple library for working with data that can be represented as a set of points on a straight line.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/AlbertSabirzianov/diapasons',
  packages=find_packages(),
  install_requires=['pydantic>=2.6'],
  classifiers=[
    'Programming Language :: Python :: 3.12',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='diapasons sections lines points ',
  project_urls={
    'GitHub': 'https://github.com/AlbertSabirzianov/diapasons'
  },
  python_requires='>=3.6'
)