from setuptools import setup, find_packages
import os

version = '0.1'

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
      author='Victor BAUMANN',
      author_email='v.baumann@4teamwork.ch',
      url='http://svn.plone.org/svn/plone/plone.example',
      license='4teamwork',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['egov'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'simplelayout.types.common'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
