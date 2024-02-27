import os
import re
import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()

    return re.search('__version__ = [\'"]([^\'"]+)[\'"]', init_py).group(1)


version = get_version('wcd_jet_sidebar')


setuptools.setup(
    name='wc-django-jet-sidebar',
    version=version,
    author='Kate Sychova',
    author_email='katuxadmitr@gmail.com',
    license='MIT License',
    description='Configurable sidebar for django-jet admin panel.',
    # install_requires=(
    #     'px-domains==0.1.4',
    # ),
    # extras_require={
    #     'dev': (
    #         'pytest>=6.0,<7.0',
    #         'pytest-watch>=4.2,<5.0',
    #         'pytest-django>=4.3,<5.0',
    #         'django-environ==0.4.5',
    #         'django-stubs',
    #         'django>=2.2,<4',
    #         'twine',
    #     ),
    # },
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=(
        'tests', 'tests.*', 'pilot',
    )),
    python_requires='>=3.6',
    classifiers=(
        'Development Status :: 2 - Pre-Alpha',

        'Programming Language :: Python :: 3',

        'Intended Audience :: Developers',
        'Topic :: Utilities',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
