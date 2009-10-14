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

from zope.interface import alsoProvides, noLongerProvides
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable

from collective.pdfpeek.transforms import convertPDFToPNG
from collective.pdfpeek.interfaces import IPDF


def pdf_changed(content, event):
    """
    This event handler is fired when ATFile objects are initialized or edited
    and calls the appropriate functions to convert the pdf to png thumbnails
    and store the list of thumbnails annotated on the file object.
    """

    if content.getContentType() == 'application/pdf':
        """Mark the object with the IPDF marker interface."""
        alsoProvides(content, IPDF)
        pdf_file_data_string = content.getFile().data
        image_converter = convertPDFToPNG()
        images = image_converter.generate_thumbnails(pdf_file_data_string)
        alsoProvides(content, IAttributeAnnotatable)
        annotations = IAnnotations(content)
        annotations['pdfpeek'] = {}
        annotations['pdfpeek']['image_thumbnails'] = images
    else:
        # a file was uploaded that is not a PDF
        # remove the marker interface
        noLongerProvides(content, IPDF)
        # remove the annotated images
        IAnnotations(content)
        annotations = IAnnotations(content)
        if 'pdfpeek' in annotations:
            del annotations['pdfpeek']

    return None
