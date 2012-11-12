from setuptools import setup, find_packages
import os


tests_require = [
    'collective.testcaselayer',
    'Plone',
    ]


def read(*rnames):
    return open('/'.join(rnames)).read()

version = '1.1.1.dev0'
maintainer = 'Mathias Leimgruber'


setup(name='ftw.globalstatusmessage',
      version=version,
      description="Shows a global message on every site.",
      long_description=open("README.rst").read() + "\n" + \
          open(os.path.join("docs", "HISTORY.txt")).read(),

      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],

      keywords='ftw global status message plone',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      url='https://github.com/4teamwork/ftw.globalstatusmessage',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,

      install_requires=[
        'setuptools',
        'z3c.autoinclude',
        'plone.z3cform',
        # -*- Extra requirements: -*-
        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),

      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
