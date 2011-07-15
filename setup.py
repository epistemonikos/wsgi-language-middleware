from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='language_middleware',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='wsgi middleware language i18n translation',
      author='Daniel P\xc3\xa9rez Rada',
      author_email='daniel at etiqs com',
      url='https://github.com/dperezrada/wsgi-language-middleware',
      license='GNU Public License v3.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
