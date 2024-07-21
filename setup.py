from distutils.core import setup
from setuptools import find_packages

setup(name='csms',
      version='0.0.1',
      packages=find_packages(include=['csms', 'csms.*']),
      install_requires=[
        'websockets==12.0',
        'ocpp==1.0.0',
      ],
      entry_points={
        'console_scripts': ['csms=csms.app.csms:main']
      })
