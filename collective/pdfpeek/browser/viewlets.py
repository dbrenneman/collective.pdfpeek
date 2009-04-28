##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""
PdfPeek Viewlets
"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase

class PdfpeekViewlet(ViewletBase):
    """This viewlet displays the pdfpeek interface
    """
    def update(self):
        """
        Arguments:
        - `self`:
        """

    index = ViewPageTemplateFile('templates/pdfpeek.pt')

class PdfpeekJavaScriptViewlet(ViewletBase):
    """This viewlet injects the lightbox2 javascript into the
    plone.htmlhead viewlet manager, just after the plone.resourceregistries
    the order is configured in profiles/default/viewlets.xml, registration in
    browser/configure.zcml
    """
    def update(self):
        """
        """

    index = ViewPageTemplateFile('templates/pdfpeek_javascript.pt')
