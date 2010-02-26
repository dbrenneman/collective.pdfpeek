##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""pdfpeek interfaces"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

from zope import schema
from zope.interface import Interface
from Products.CMFPlone import PloneMessageFactory as _


class IPDF(Interface):
    """Marker interface denoting a pdf document."""


class IConvertPDFToImage(Interface):
    """Marker interface identifying the pdf image thumbnail generator."""


class IPDFPeekConfiguration(Interface):
    """interface describing the pdfpeek control panel."""
    # toggle image preview viewlet on/off
    # control size of image preview
    # control size of image thumbnail

    preview_toggle = schema.Bool(title=_(u'Preview Toggle'),
                                 description=_(
        u'Display PDFPeek image previews in default content views.'),
                                 required=True,
                                 default=True)

    eventhandler_toggle = schema.Bool(title=_(u'Event Handler Toggle'),
                                 description=_(
        u'Enable the default PDFPeek event handler.'),
                                 required=True,
                                 default=True)

    preview_length = schema.Int(
        title=_(u'Preview Length'),
        description=_(u'Control PDFPeek Image Preview Length.'),
        required=True,
        default=512,
        )

    preview_width = schema.Int(
        title=_(u'Preview Width'),
        description=_(u'Control PDFPeek Image Preview Width.'),
        required=True,
        default=512,
        )

    thumbnail_length = schema.Int(
        title=_(u'Thumbnail Length'),
        description=_(u'Control PDFPeek Image Thumbnail Length.'),
        required=True,
        default=128,
        )

    thumbnail_width = schema.Int(
        title=_(u'Thumbnail Width'),
        description=_(u'Control PDFPeek Image Thumbnail Width.'),
        required=True,
        default=128,
        )
