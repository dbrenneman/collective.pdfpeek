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
    contact_email = schema.Text(title=_(u'PDF Peek Configuration'),
                                 description=_(
        u'PDF Peek configuration text.'),
                                 required=False,
                                 default=u'')



