from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


def sites_vocabulary_factory(_records_proxy):
    portal = getSite()
    terms = [SimpleTerm('/'.join(portal.getPhysicalPath()),
                        title=portal.Title())]

    catalog = getToolByName(portal, 'portal_catalog')
    query = {
        'object_provides': [
            'plone.app.layout.navigation.interfaces.INavigationRoot'],
        'sort_on': 'sortable_title'}

    for brain in catalog(query):
        terms.append(SimpleTerm(brain.getPath(), title=brain.Title))

    return SimpleVocabulary(terms)
