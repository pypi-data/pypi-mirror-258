from setuptools import setup, find_packages
excluded_packages = [
    'core', 'core.*', 
    'linkzone', 'linkzone.*', 
]
setup(
    name='stela_professional',
    version='0.3.81',
    packages=find_packages(exclude=excluded_packages),
    include_package_data=True,
    license='MIT',
    description='All apps in one for business.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'Babel',
        'beautifulsoup4',
        'bleach',
        'boto3',
        'cryptography',
        'pycryptodome',
        'Django',
        'django-cities-light',
        'django-ckeditor',
        'django-crispy-forms',
        'django-cron',
        'django-environ',
        'django-hosts',
        'django-restframework',
        'django-storages',
        'google-api-python-client',
        'facebook-business',
        'gunicorn',
        'jwt',
        'openai',
        'paypal-checkout-serversdk',
        'paypalrestsdk',
        'phonenumbers',
        'crispy-bootstrap4',
        'Pillow',
        'python-amazon-paapi',
        'psycopg2-binary',
        'stripe',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)