from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common


class StatusmessageViewlet(common.PathBarViewlet):
    render = ViewPageTemplateFile('statusmessage.pt')
