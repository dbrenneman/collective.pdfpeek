from zope.i18nmessageid import MessageFactory

PDFPeekMessageFactory = MessageFactory('collective.pdfpeek')

def initialize(context):
    """Intializer called when used as a Zope 2 product."""
