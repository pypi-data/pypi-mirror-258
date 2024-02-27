import os
from setuptools import setup

if os.getenv('MY_AIMINIFY_PACKAGE_UPLOAD_MODE'):
    setup(
        name='aiminify',
        version='0.0.1a3',
        license='',
        description='',
        author='aiminify',
        author_email='support@aiminify.com',
        url='',
    ) 
raise Exception("This package should not be installed. Contact support@aiminify.com for further information.")

