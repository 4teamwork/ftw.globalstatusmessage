Introduction
============

With ``ftw.globalstatusmessage`` a Plone site administrator display messages
on all pages.

This is useful for inform the users about an upcoming maintance downtime or
any other important thing.

The message can be changed in the plone control panel:


.. image:: https://raw.github.com/4teamwork/ftw.globalstatusmessage/master/docs/screenshot.png


Compatibility
=============

Plone 4.1

.. image:: https://jenkins.4teamwork.ch/job/ftw.globalstatusmessage-master-test-plone-4.1.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.globalstatusmessage-master-test-plone-4.1.x.cfg

Plone 4.2

.. image:: https://jenkins.4teamwork.ch/job/ftw.globalstatusmessage-master-test-plone-4.2.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.globalstatusmessage-master-test-plone-4.2.x.cfg

Plone 4.3

.. image:: https://jenkins.4teamwork.ch/job/ftw.globalstatusmessage-master-test-plone-4.3.x.cfg/badge/icon
   :target: https://jenkins.4teamwork.ch/job/ftw.globalstatusmessage-master-test-plone-4.3.x.cfg


Installation
============

- Add ``ftw.globalstatusmessage`` to your buildout configuration:

::

    [instance]
    eggs +=
        ftw.globalstatusmessage

- Install the generic import profile.


Uninstall
=========

This package provides an uninstall Generic Setup profile.
Uninstall the package by using Plone's addon controlpanel or portal_quickInstaller.



Links
=====

- Main github project repository: https://github.com/4teamwork/ftw.globalstatusmessage
- Issue tracker: https://github.com/4teamwork/ftw.globalstatusmessage/issues
- Package on pypi: http://pypi.python.org/pypi/ftw.globalstatusmessage
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.globalstatusmessage


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.globalstatusmessage`` is licensed under GNU General Public License, version 2.
