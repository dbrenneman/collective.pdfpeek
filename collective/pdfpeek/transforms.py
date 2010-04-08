##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

"""
PDF to Image Converter Class
"""

__author__ = """David Brenneman <db@davidbrenneman.com>"""
__docformat__ = 'plaintext'

import logging
import subprocess
import cStringIO

import pyPdf
from PIL import Image

from zope.interface import implements
from zope.component import getUtility
from zope.app.component.hooks import getSite
from OFS.Image import Image as OFSImage

from collective.pdfpeek.interfaces import IConvertPDFToImage
from collective.pdfpeek.interfaces import IPDFPeekConfiguration

logger = logging.getLogger('collective.pdfpeek')


class convertPDFToImage(object):
    """
    utility for converting each page of a pdf file to an image file
    returns a list of images, one per page of the pdf file
    """
    implements(IConvertPDFToImage)

    def ghostscript_transform(self, pdf, page_num):
        """
        ghostscript_transform takes an AT based object with an IPDF interface
        and a page number argument and converts that page number of the pdf
        file to a png image file.
        """
        first_page = "-dFirstPage=%s" % (page_num)
        last_page = "-dLastPage=%s" % (page_num)
        gs_cmd = [
            "gs",
            "-q",
            "-sDEVICE=jpeg",
            "-dJPEGQ=99",
            "-dGraphicsAlphaBits=4",
            "-dTextAlphaBits=4",
            "-dDOINTERPOLATE",
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            first_page,
            last_page,
            "-r59x56",
            "-sOutputFile=%stdout",
            "-",
            ]

        jpeg = None
        """run the ghostscript command on the pdf file,
        capture the output png file of the specified page number"""
        gs_process = subprocess.Popen(gs_cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE,)
        gs_process.stdin.write(pdf)
        jpeg = gs_process.communicate()[0]
        gs_process.stdin.close()
        return_code = gs_process.returncode
        if return_code == 0:
            logger.info("Ghostscript processed one page of a pdf file.")
        else:
            logger.warn("Ghostscript process did not exit cleanly! Error Code: %d" % (return_code))
            jpeg = None
        return jpeg

    #check if the pdf is corrupted, and try to fix it...
    def fixPdf(self, string):
        try:
            result = string + "\n%%EOF\n"
            return result
        except Exception, e:
            logger.error("Unable to fix pdf file.")
            return string

    def generate_thumbnails(self, pdf_file_data_string):
        document_page_count = 0
        page_number = 0
        images = None
        pdf = None
        pdf_file_data_string = str(pdf_file_data_string)
        """If the file is a pdf file then we look inside with PyPDF and see
        how many pages there are.
        """
        # if we've got a pdf file,
        # get the pdf file as a file object containing the data in a string
        # pdf_file_object = StringIO.StringIO(pdf_file_data_string)
        # create a pyPdf object from the pdf file data
        try:
            pdf = pyPdf.PdfFileReader(cStringIO.StringIO(pdf_file_data_string))
        except:
            logger.warn("error opening pdf file, trying to fix it...")
            fixed_pdf_string = self.fixPdf(pdf_file_data_string)
            #try to reopen the pdf file again
            try:
                pdf = pyPdf.PdfFileReader(cStringIO.StringIO(fixed_pdf_string))
            except:
                logger.warn("this pdf file cannot be fixed.")

        if pdf.isEncrypted:
            try:
                decrypt = pdf.decrypt('')
                if decrypt == 0:
                    logger.warn("This pdf is password protected.")
            except:
                logger.warn("Errors have been found while attempting to decrypt the pdf file.")

        if pdf:
            # get the number of pages in the pdf file from the pyPdf object
            document_page_count = pdf.getNumPages()
            logger.info("Found a PDF file with %d pages." % (document_page_count))
            if document_page_count > 0:
                portal = getSite()
                config = getUtility(
                    IPDFPeekConfiguration,
                    name='pdfpeek_config',
                    context=portal
                    )
                # if we're dealing with a pdf file,
                # set the thumbnail size
                thumb_size = (config.thumbnail_width, config.thumbnail_length)
                preview_size = (config.preview_width, config.preview_length)
                # set up the images dict
                images = {}

                for page in range(document_page_count):
                    # for each page in the pdf file,
                    # set up a human readable page number counter starting at 1
                    page_number = page + 1
                    # set up the image object ids and titles
                    image_id = "%d_preview" % page_number
                    image_title = "Page %d Preview" % page_number
                    image_thumb_id = "%d_thumb" % page_number
                    image_thumb_title = "Page %d Thumbnail" % page_number
                    # create a file object to store the thumbnail and preview in
                    raw_image_thumb = cStringIO.StringIO()
                    raw_image_preview = cStringIO.StringIO()
                    # run ghostscript, convert pdf page into image
                    raw_image = self.ghostscript_transform(
                        pdf_file_data_string, page_number)
                    # use PIL to generate thumbnail from jpeg
                    img_thumb = Image.open(cStringIO.StringIO(raw_image))
                    img_thumb.thumbnail(thumb_size, Image.ANTIALIAS)
                    # save the resulting thumbnail in the file object
                    img_thumb.save(raw_image_thumb, "JPEG")
                    # use PIL to generate preview from jpeg
                    img_preview = Image.open(cStringIO.StringIO(raw_image))
                    img_preview.thumbnail(preview_size, Image.ANTIALIAS)
                    # save the resulting thumbnail in the file object
                    img_preview.save(raw_image_preview, "JPEG")
                    # create the OFS.Image objects
                    image_full_object = OFSImage(image_id, image_title, raw_image_preview)
                    image_thumb_object = OFSImage(image_thumb_id, image_thumb_title, raw_image_thumb)
                    # add the objects to the images dict
                    images[image_id] = image_full_object
                    images[image_thumb_id] = image_thumb_object
                    logger.info("Thumbnail generated.")
            else:
                    logger.error("Error: %d pages in PDF file." % (document_page_count))
        return images
