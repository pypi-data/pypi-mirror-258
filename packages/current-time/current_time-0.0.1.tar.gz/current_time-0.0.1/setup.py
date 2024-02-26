from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='current_time',
  version='0.0.1',
  description='Time Display',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Stephen Angelo',
  author_email='stephenangeloirl@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='timedisplay', 
  packages=find_packages(),
  install_requires=[''] 
)
