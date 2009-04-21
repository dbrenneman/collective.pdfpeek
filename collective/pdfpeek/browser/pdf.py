from Acquisition import aq_inner

from Products.Five.browser import BrowserView

from plone.memoize.instance import memoize

class PDFImageAnnotationView(BrowserView):
    """view class used to access the image thumbnails that pdfpeek annotates on ATFile objects.
    """
    
    @memoize
    def pdf_image_annotation(self):
        context = aq_inner(self.context)
        annotations = dict(context.__annotations__)
        images = annotations['pdfpeek']['image_thumbnails']
        return images

