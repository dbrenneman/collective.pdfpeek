##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""
PDFpeek browser view interfaces
"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

from zope.interface import Interface

class IPDFpeekLayer(Interface):
    """Marker interface that defines a Zope 3 browserlayer.
    """
