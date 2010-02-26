##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""
PDFpeek Event Handlers
"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

import logging

from zope.component import getUtility
from zope.app.component.hooks import getSite
from zope.interface import alsoProvides, noLongerProvides
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable

from collective.pdfpeek.transforms import convertPDFToImage
from collective.pdfpeek.interfaces import IPDF
from collective.pdfpeek.interfaces import IPDFPeekConfiguration
from collective.pdfpeek.async import get_queue, Job
from collective.pdfpeek.conversion import convert_pdf_to_image, remove_image_previews 

logger = logging.getLogger('collective.pdfpeek.browser.utils')


def pdf_changed(content, event):
    """
    This event handler is fired when ATFile objects are initialized or edited
    and calls the appropriate functions to convert the pdf to png thumbnails
    and store the list of thumbnails annotated on the file object.
    """
    portal = getSite()
    if 'collective.pdfpeek' in portal.portal_quickinstaller.objectIds():
        config = getUtility(IPDFPeekConfiguration, name='pdfpeek_config', context=portal)
        if config.eventhandler_toggle == True:
            if content.getContentType() == 'application/pdf':
                """Mark the object with the IPDF marker interface."""
                alsoProvides(content, IPDF)
                pdf_file_data_string = content.getFile().data
                image_converter = convertPDFToImage()
                images = image_converter.generate_thumbnails(pdf_file_data_string)
                alsoProvides(content, IAttributeAnnotatable)
                annotations = IAnnotations(content)
                annotations['pdfpeek'] = {}
                annotations['pdfpeek']['image_thumbnails'] = images
            else:
                noLongerProvides(content, IPDF)
                IAnnotations(content)
                annotations = IAnnotations(content)
                if 'pdfpeek' in annotations:
                    del annotations['pdfpeek']
        return None


def queue_document_conversion(content, event):
    """
    This method queues the document for conversion.
    One job is queued for the jodconverter if required, and for pdfpeek.
    """
    portal = getSite()
    if 'collective.pdfpeek' in portal.portal_quickinstaller.objectIds():
        ALLOWED_CONVERSION_TYPES = ['application/pdf']
        # if we have a document in the file field, add the jobs to the queue
        content_type = content.getFile().getContentType()
        if (content_type in ALLOWED_CONVERSION_TYPES):
            # get the queue
            conversion_queue = get_queue('collective.pdfpeek.conversion')
            # create a jodconverter job
            converter_job = Job(convert_pdf_to_image, content)
            # add it to the queue
            conversion_queue.pending.append(converter_job)
            logger.info("Document Conversion Job Queued")
        else:
            queue_image_removal(content)


def queue_image_removal(content):
    """
    Queues the image removal if there is no longer a pdf
    file stored on the object
    """
    conversion_queue = get_queue('collective.pdfpeek.conversion')
    removal_job = Job(remove_image_previews, content)
    conversion_queue.pending.append(removal_job)
    logger.info("Document Preview Image Removal Job Queued")
