from contextlib import contextmanager
from zope.browser.interfaces import IBrowserView
from zope.component import getGlobalSiteManager
from zope.interface import Interface


@contextmanager
def view_registered(factory, name, required=(Interface, Interface)):
    options = dict(
        factory=factory,
        required=required,
        provided=IBrowserView,
        name=name,
    )
    getGlobalSiteManager().registerAdapter(**options)
    try:
        yield
    finally:
        getGlobalSiteManager().unregisterAdapter(**options)
