# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import getFSVersionTuple

PROJECTNAME = 'ftw.globalstatusmessage'

if getFSVersionTuple() > (5, ):
    IS_PLONE_5 = True
else:
    IS_PLONE_5 = False
