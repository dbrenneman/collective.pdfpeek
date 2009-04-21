##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""
PdfPeek browser view interfaces
"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

from plone.theme.interfaces import IDefaultPloneLayer

class IPdfPeekThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
       If you need to register a viewlet only for the
       "PdfPeek" skin, this interface must be its layer
       (in viewlets/configure.zcml).
    """
