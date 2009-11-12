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


class IConvertPDFToPNG(Interface):
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

#     preview_size = schema.Text(title=_(u'Preview Size'),
#                                  description=_(
#         u'Control PDFPeek Image Preview Size.'),
#                                  required=False,
#                                  default=u'')

#     thumbnail_size = schema.Text(title=_(u'Thumbnail Size'),
#                                  description=_(
#         u'Control PDFPeek Image Thumbnail Size.'),
#                                  required=False,
#                                  default=u'')
