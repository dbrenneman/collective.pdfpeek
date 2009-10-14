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

import subprocess
import StringIO

import pyPdf
from PIL import Image

from zope.interface import implements
from OFS.Image import Image as OFSImage

from collective.pdfpeek.interfaces import IConvertPDFToPNG


class convertPDFToPNG(object):
    """
    utility for converting each page of a pdf file to an image file
    returns a list of images, one per page of the pdf file
    """
    implements(IConvertPDFToPNG)

    def ghostscript_transform(self, pdf_file_data_string, page_num):
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
            "-r55W56",
            "-sOutputFile=%stdout",
            "-",
            ]

        jpeg = None
        """run the ghostscript command on the pdf file,
        capture the output png file of the specified page number"""
        gs_process = subprocess.Popen(gs_cmd,stdout=subprocess.PIPE,stdin=subprocess.PIPE,)
        gs_process.stdin.write(pdf_file_data_string.getvalue())
        jpeg = gs_process.communicate()[0]
        gs_process.stdin.close()
        return_code = gs_process.returncode
        if return_code == 0:
            return jpeg
        else:
            print "Warning: ghostscript process did not exit cleanly! Error Code: %d" % (return_code)
            raise Exception

    def generate_thumbnails(self, pdf_file):
        document_page_count = 0
        page_number = 0
        images = None
        """If the file is a pdf file then we look inside with PyPDF and see
        how many pages there are.
        """
        # if we've got a pdf file,
        # get the pdf file as a file object containing the data in a string
        pdf_file_data_string = StringIO.StringIO(pdf_file.getFile().data)
        # create a pyPdf object from the pdf file data
        pdf = pyPdf.PdfFileReader(pdf_file_data_string)
        # get the number of pages in the pdf file from the pyPdf object
        document_page_count = pdf.getNumPages()
        print "Found a PDF file with %d pages." % (document_page_count)
        images = None
        if document_page_count > 0:
            # if we're dealing with a pdf file,
            # set the thumbnail size
            thumb_size = 128, 128
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
                # create a file object to store the thumbnail in
                raw_image_thumb = StringIO.StringIO('')
                # run ghostscript, convert pdf page into image
                raw_image = self.ghostscript_transform(
                                pdf_file_data_string, page_number)
                # use PIL to generate thumbnail from jpeg
                img_thumb = Image.open(StringIO.StringIO(raw_image))
                img_thumb.thumbnail(thumb_size, Image.ANTIALIAS)
                # save the resulting thumbnail in the file object
                img_thumb.save(raw_image_thumb, "JPEG")
                # create the OFS.Image objects
                image_full_object = OFSImage(image_id, image_title, raw_image)
                image_thumb_object = OFSImage(image_thumb_id, image_thumb_title, raw_image_thumb)
                # add the objects to the images dict
                images[image_id] = image_full_object
                images[image_thumb_id] = image_thumb_object
                print "Thumbnail generated."
        else:
            print "Error: %d pages in PDF file." % (document_page_count)
        return images
