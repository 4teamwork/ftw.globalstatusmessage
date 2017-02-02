Introduction
============

With ``ftw.globalstatusmessage`` a Plone site administrator display messages
on all pages.

This is useful for inform the users about an upcoming maintance downtime or
any other important thing.

The message can be changed in the plone control panel:


.. image:: https://raw.githubusercontent.com/4teamwork/ftw.globalstatusmessage/master/docs/screenshot.png

Exclude sites
-------------

With the ``Exclude sites`` option it is possible to show the global status
message only for certain sub sites.
All containers providing the interface ``INavigationRoot`` are considered
sub sites. Make sure that the ``object_provides`` catalog index is up to date
after enabling the interface for a container.

When having nested sub sites, the nearest parent sub site relative to the
current context is relevant.
If the nearest sub site is not excluded but a parent is excluded, the message
is shown on the current context.


Compatibility
=============

Supports Plone `4.2`, `4.3`.


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

- Github: https://github.com/4teamwork/ftw.globalstatusmessage
- Issues: https://github.com/4teamwork/ftw.globalstatusmessage/issues
- Pypi: http://pypi.python.org/pypi/ftw.globalstatusmessage
- Continuous integration: https://jenkins.4teamwork.ch/search?q=ftw.globalstatusmessage


Copyright
=========

This package is copyright by `4teamwork <http://www.4teamwork.ch/>`_.

``ftw.globalstatusmessage`` is licensed under GNU General Public License, version 2.
