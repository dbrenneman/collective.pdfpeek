from zope.interface import implements
from zope.component import adapts

from zope.traversing.interfaces import ITraversable
from zope.publisher.interfaces.http import IHTTPRequest

from collective.pdfpeek.interfaces import IPDF

class PDFPeekImageScaleTraverser(object):
    """Used to traverse to images stored on IPDF objects
    
    Traversing to portal/object/++images++/++page++1 will retrieve the first
    page of the pdf, acquisition-wrapped.
    """
    implements(ITraversable)
    adapts(IPDF, IHTTPRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        
    def traverse(self, name, ignore):
        annotations = dict(self.context.__annotations__)
        image = annotations['pdfpeek']['image_thumbnails'][name]
        return image


