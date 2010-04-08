import logging

from zope.interface import alsoProvides, noLongerProvides
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable

from collective.pdfpeek.transforms import convertPDFToImage
from collective.pdfpeek.interfaces import IPDF

logger = logging.getLogger('collective.pdfpeek.conversion')


def convert_pdf_to_image(content):
    """
    """
    msg = "Converting pdf file."
    logger.info(msg)
    content_type = content.getFile().getContentType()
    if content_type == "application/pdf":
        pdf_file_data_string = str(content.getFile())
        msg = "Got A PDF file."
        logger.info(msg)
        msg = run_pdfpeek(content, pdf_file_data_string)
    return msg


def run_pdfpeek(content, pdf_file_data_string):
    image_converter = convertPDFToImage()
    images = None
    errmsg = "Failed to convert PDF to images with PDFPeek on %s." % content.id
    successmsg = "Converted PDF to images with PDFPeek on %s." % content.id

    try:
        images = image_converter.generate_thumbnails(pdf_file_data_string)
    except:
        logger.error(errmsg)

    if images:
        alsoProvides(content, IPDF)
        alsoProvides(content, IAttributeAnnotatable)
        annotations = IAnnotations(content)
        annotations['pdfpeek'] = {}
        annotations['pdfpeek']['image_thumbnails'] = images
        logger.info(successmsg)
        return successmsg
    else:
        return errmsg


def remove_image_previews(content):
    """
    This function removes the image preview annotations if a pdf file is
    removed
    """
    # a file was uploaded that is not a PDF
    # remove the pdf file
    content.filepreview = None
    # remove the marker interface
    noLongerProvides(content, IPDF)
    # remove the annotated images
    IAnnotations(content)
    annotations = IAnnotations(content)
    if 'pdfpeek' in annotations:
        del annotations['pdfpeek']
    msg = "Removed preview annotations from %s." % content.id
    logger.info(msg)
    return msg
