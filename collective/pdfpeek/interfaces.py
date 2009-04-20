##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""pdfpeek interfaces"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class ILayer(Interface):
    """Marker interface that will be applied to the request when this product is installed."""

class IPDF(Interface):
    """Marker interface denoting a pdf document."""

class IConvertPDFToPNG(Interface):
    """Marker interface identifying the pdf image thumbnail generator."""

