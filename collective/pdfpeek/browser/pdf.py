##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from plone.memoize.instance import memoize

from collective.pdfpeek.interfaces import IPDF

class PdfImageAnnotationView(BrowserView):
    """view class used to access the image thumbnails that pdfpeek annotates on ATFile objects.
    """
    
    @memoize
    def pdf_image_annotation(self, page_number=0):
        context = aq_inner(self.context)
        annotations = dict(context.__annotations__)
        images = annotations['pdfpeek']['image_thumbnails']
        return images[page_number]
    

class IsPdfView(BrowserView):
    """check to see if the object is a PDF
    """
    @property    
    def is_pdf(self):
        if IPDF.providedBy(self.context):
            return True
        return False
    
