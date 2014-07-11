from setuptools import setup, find_packages
import os

version = '1.6.3.dev0'
maintainer = 'Mathias Leimgruber'

tests_require = ['plone.app.testing',]

extras_require = {
    'tests': tests_require,
    }
setup(name='egov.contactdirectory',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/egov.contactdirectory',
      license='4teamwork',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['egov'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'simplelayout.base',
          'simplelayout.types.common',
          'ftw.table',
          'ftw.tabbedview',
          'ftw.upgrade',
          'ftw.geo',
          # -*- Extra requirements: -*-
      ],

      tests_require=tests_require,
      extras_require=extras_require,

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
