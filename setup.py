from setuptools import setup, find_packages
import os

version = '1.7.0'
maintainer = 'Mathias Leimgruber'

tests_require = ['plone.app.testing',
                 'ftw.builder',
                 'ftw.testbrowser',
                 'ftw.zipexport']

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
      author='4teamwork AG',
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
      extras_require=dict(tests=tests_require,
                          zip_export=['ftw.zipexport']),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
