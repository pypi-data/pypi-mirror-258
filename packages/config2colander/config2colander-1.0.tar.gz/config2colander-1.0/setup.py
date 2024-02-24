from setuptools import setup,find_packages


import os
here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.md'), 'r').read()
changelog = open(os.path.join(here, 'CHANGELOG.md'), 'r').read()

setup(name='config2colander',
  version='1.0',
  description='create a deform/colander schema from json configuration',
  long_description=readme + "\n\n\n" + changelog,
  long_description_content_type="text/markdown",
  author='pdepmcp',
  author_email='pdepmcp@gmail.com',
  license='MIT',
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.9',
  ],
  keywords="pyramid module deform/colander schema",
  python_requires='>=3.7',
  url='http://www.pingpongstars.it',
  install_requires=['deform','pyramid>=1.1' ],
  #packages=['src/test1'],
  packages=find_packages(),
  include_package_data=True,

)


