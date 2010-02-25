##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

from Acquisition import aq_inner
from zope.component import getUtility
from zope.app.component.hooks import getSite
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from OFS.SimpleItem import SimpleItem
from Products.Five.browser import BrowserView
from zope.formlib.form import FormFields
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.controlpanel.form import ControlPanelForm
from collective.pdfpeek.interfaces import IPDFPeekConfiguration
from collective.pdfpeek.interfaces import IPDF


class PdfImageAnnotationView(BrowserView):
    """view class used to access the image thumbnails that pdfpeek annotates on ATFile objects.
    """

    @property
    def num_pages(self):
        context = aq_inner(self.context)
        annotations = dict(context.__annotations__)
        if annotations['pdfpeek']['image_thumbnails']:
            annotations_len = len(annotations['pdfpeek']['image_thumbnails'])
            num_pages = range(annotations_len / 2)
        else:
            num_pages = 0
        return num_pages


class IsPdfView(BrowserView):
    """check to see if the object is a PDF
    """

    @property
    def is_pdf(self):
        if IPDF.providedBy(self.context):
            return True
        return False


class IsPreviewOnView(BrowserView):
    """
    check to see if the image previews are on.
    """

    @property
    def previews_on(self):
        portal = getSite()
        config = getUtility(IPDFPeekConfiguration, name='pdfpeek_config', context=portal)

        if config.preview_toggle == True:
            return True
        return False


class PDFPeekControlPanel(ControlPanelForm):
    """Control panel form for setting pdfpeek image and thumbnail sizes"""
    form_fields = FormFields(IPDFPeekConfiguration)
    label = _(u'PDF Peek Settings')
    description = _(u'Global settings for the PDF Peek Product')
    form_name = _(u'PDF Peek Settings')


class PDFPeekConfiguration(SimpleItem):
    implements(IPDFPeekConfiguration)
    preview_toggle = FieldProperty(IPDFPeekConfiguration['preview_toggle'])
    eventhandler_toggle = FieldProperty(IPDFPeekConfiguration['eventhandler_toggle'])
    preview_length = FieldProperty(IPDFPeekConfiguration['preview_length'])
    preview_width = FieldProperty(IPDFPeekConfiguration['preview_width'])
    thumbnail_length = FieldProperty(IPDFPeekConfiguration['thumbnail_length'])
    thumbnail_width = FieldProperty(IPDFPeekConfiguration['thumbnail_width'])


def form_adapter(context):
    portal = getSite()
    return getUtility(IPDFPeekConfiguration, name='pdfpeek_config', context=portal)
