from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='fificord.py',
  version='1.0.0',
  description='fificord.py is a better discord.py alternative.',
  long_description_content_type="text/x-rst",
  long_description=open("README.rst", "r").read(),
  url='',  
  author='maxeqx',
  author_email='maxeqxmail@gmail.com',
  license='MIT',
  classifiers=classifiers,
  keywords='discord discord.py nextcord nextcord.py discord.py-self discord-self selfbot self bot',
  packages=find_packages(),
  install_requires=['tls_client', 'maxdev', 'asyncio'] 
)