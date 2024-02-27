import os
from setuptools import setup

if not os.getenv('MY_AIMINIFY_PACKAGE_UPLOAD_MODE'):
    raise Exception("This package should not be installed. Contact support@aiminify.com for further information.")

setup(

    name='aiminify',
    version='0.0.1a2',
    license='',
    description='',
    author='aiminify',
    author_email='support@aiminify.com',
    url='',
)