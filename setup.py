""" CodeMommy WebPython """

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='CodeMommyWebPython',
      version='0.0.3',
      url='http://www.CodeMommy.com',
      license='Apache 2.0',
      description='Web MVC framework of light and fast',
      long_description='Web MVC framework of light and fast',
      author='Candison',
      author_email='kandisheng@163.com',
      maintainer='Candison',
      maintainer_email='kandisheng@163.com',
      platforms=['Any'],
      packages=['CodeMommy', 'CodeMommy/core'],
      install_requires=['jinja2>=2.9.5'],
      classifiers=[]
      )
