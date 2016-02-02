from setuptools import setup, find_packages
import sys, os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.6'

setup(
      name='language_middleware',
      version=version,
      description="This Wsgi middleware, takes the language from urls similiar to '/es/documents' or from the Accept language header.",
      long_description=read('README.md'),
      classifiers=[
            "Development Status :: 4 - Beta",
            "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: GNU General Public License (GPL)",
      ],
      keywords='wsgi middleware language i18n translation',
      author='Daniel Perez Rada',
      author_email='dperezrada at gmail',
      url='https://github.com/dperezrada/wsgi-language-middleware',
      license='GNU Public License v3.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      tests_require=['nose >= 0.11', 'mock', 'mako'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      test_suite="tests",
      entry_points="""
      # -*- Entry points: -*-
      """,
)
