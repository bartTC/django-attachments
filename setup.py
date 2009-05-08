from setuptools import setup, find_packages

setup(
    name='django-attachments',
    version='0.2.3',
    description='A generic Django application to attach Files (Attachments) to any model',
    long_description=open('README.rst').read(),
    author='Martin Mahner',
    author_email='martin@mahner.org',
    url='http://github.com/bartTC/django-attachments/tree/master',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    package_data = {
        'attachments': [
            'templates/attachments/*.html',
        ]
    },
    zip_safe=False,
)
