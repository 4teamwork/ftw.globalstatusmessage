from setuptools import setup, find_packages
import os


tests_require = [
    'AccessControl',
    'ftw.builder',
    'ftw.testbrowser',
    'ftw.testing',
    'ftw.publisher.sender',
    'ftw.publisher.receiver',
    'plone.app.testing',
    'unittest2',
    'zope.configuration',
    ]


def read(*rnames):
    return open('/'.join(rnames)).read()

version = '1.7.2'
maintainer = 'Mathias Leimgruber'


setup(name='ftw.globalstatusmessage',
      version=version,
      description="Shows a global message on every site.",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers

      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='ftw global status message plone',
      author='4teamwork AG',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.globalstatusmessage',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'Plone',
        'Products.CMFCore',
        'Products.CMFPlone',
        'Products.GenericSetup',
        'Zope2',
        'ftw.upgrade',
        'plone.api',
        'plone.app.layout',
        'plone.app.registry',
        'plone.registry',
        'plone.supermodel',
        'plone.z3cform',
        'setuptools',
        'z3c.form',
        'zope.component',
        'zope.i18nmessageid',
        'zope.interface',
        'zope.schema',
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
