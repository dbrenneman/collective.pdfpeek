##########################################################################
#                                                                        #
#        copyright (c) 2010 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

import logging

import transaction
from zope.component import getSiteManager
from zope.component import getUtility
from zope.component import queryUtility
from zope.app.component.hooks import setSite
from zope.annotation.interfaces import IAnnotations
from zope.interface import noLongerProvides
from Products.CMFCore.utils import getToolByName

from collective.pdfpeek.browser.pdf import PDFPeekConfiguration
from collective.pdfpeek.interfaces import IPDFPeekConfiguration
from collective.pdfpeek.interfaces import IPDF
from collective.pdfpeek.async import IQueue

logger = logging.getLogger('collective.pdfpeek.setuphandlers')


def importVarious(context):
    """Miscellanous steps import handle
    """

    if context.readDataFile('collective.pdfpeek_various.txt') is None:
        return

    portal = context.getSite()
    config_name = 'pdfpeek_config_' + portal.id
    sm = portal.getSiteManager()

    if not sm.queryUtility(IPDFPeekConfiguration, name=config_name):
        sm.registerUtility(
            PDFPeekConfiguration(),
            IPDFPeekConfiguration,
            config_name
            )


def uninstall(context):
    if context.readDataFile('collective.pdfpeek.uninstall.txt') is None:
        return
    unregisterUtilities(context)
    removePreviewImages(context)
    transaction.commit()


def unregisterUtilities(context):
    portal = context.getSite()
    setSite(portal)
    sm = getSiteManager(portal)
    config_name = 'pdfpeek_config_' + portal.id
    pdfpeek_config_utility = getUtility(IPDFPeekConfiguration, config_name)
    sm.unregisterUtility(pdfpeek_config_utility, IPDFPeekConfiguration)
    del pdfpeek_config_utility
    logger.info("Removed PDFpeek Configuration")
    queue_name = 'collective.pdfpeek.conversion_' + portal.id
    queue = queryUtility(IQueue, queue_name)
    if queue is not None:
        queue_utility = getUtility(IQueue, queue_name)
        sm.unregisterUtility(queue_utility, IQueue)
        del queue_utility
    logger.info("Removed PDFpeek Queue")


def removePreviewImages(context):
    catalog = getToolByName(context.getSite(), 'portal_catalog')
    pdfs = catalog(object_provides=IPDF.__identifier__)
    for pdf in pdfs:
        pdf = pdf.getObject()
        noLongerProvides(pdf, IPDF)
        logger.info("Removed IPDF interface")
        IAnnotations(pdf)
        annotations = IAnnotations(pdf)
        if 'pdfpeek' in annotations:
            del annotations['pdfpeek']
            logger.info("Removed pdf image annotations")
