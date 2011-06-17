##########################################################################
#                                                                        #
#        copyright (c) 2011 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

from plone.app.registry.browser import controlpanel

from collective.pdfpeek import PDFPeekMessageFactory as _
from collective.pdfpeek.interfaces import IPDFPeekConfiguration

class PDFPeekControlPanelEditForm(controlpanel.RegistryEditForm):
    schema = IPDFPeekConfiguration

    label = _(u"PDFPeek configuration")
    description = _(u"""""")

    def updateFields(self):
        super(PDFPeekControlPanelEditForm, self).updateFields()


    def updateWidgets(self):
        super(PDFPeekControlPanelEditForm, self).updateWidgets()


class PDFPeekControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PDFPeekControlPanelEditForm
