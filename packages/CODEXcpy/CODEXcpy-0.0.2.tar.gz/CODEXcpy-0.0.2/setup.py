from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='CODEXcpy',
  version='0.0.2',
  description='Welcome',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ankit',
  author_email='codexstudiosltd@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='CODEXcpy', 
  packages=find_packages(),
  install_requires=[''] 
)