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

from zope.interface import implements
from collective.pdfpeek.interfaces import IConvertPDFToPNG
import subprocess
import cStringIO
import pyPdf


class convertPDFToPNG(object):
    """
    utility for converting each page of a pdf file to an image file
    returns a list of images, one per page of the pdf file
    """    
    implements(IConvertPDFToPNG)
    
    def ghostscript_transform(self, pdf_file, page_num):
        """ghostscript_transform takes an ATFile object with an IPDF interface and a page number argument and converts that page number of the pdf file to a png image file."""
        first_page = "-dFirstPage=%s" % (page_num)
        last_page = "-dLastPage=%s" % (page_num)
        gs_cmd = [
            "gs",
            "-q",
            "-sDEVICE=jpeg",
            "-dJPEGQ=95",
            "-dGraphicsAlphaBits=4",
            "-dTextAlphaBits=4",
            "-dDOINTERPOLATE",
            "-dSAFER",
            "-dBATCH",
            "-dNOPAUSE",
            first_page,
            last_page,
            "-r77W78",
            "-sOutputFile=%stdout",
            "-",
            ]
        
        jpeg = None
        """run the ghostscript command on the pdf file,
        capture the output png file of the specified page number"""

        pdf_file_data = pdf_file.getFile()
        pdf_file_data_string = cStringIO.StringIO(pdf_file_data.get_data())

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
        page_number = 1
        images = None
        pdf_file_data = pdf_file.getFile()
        pdf_file_data_string = cStringIO.StringIO(pdf_file_data.get_data())
        """If the file is a pdf file then we look inside with PyPDF and see
        how many pages there are.
        """
        if pdf_file.getContentType() == 'application/pdf':
            pdf = pyPdf.PdfFileReader(pdf_file_data_string)
            document_page_count = pdf.getNumPages()
            print "Found a PDF file with %d pages." % (document_page_count)
        else:
            print "Not a PDF file."
            
        if document_page_count > 0:
            for page in range(document_page_count):
                page_number = page + 1
                images = []
                images += [self.ghostscript_transform(pdf_file, page_number)] 
                print "Thumbnail generated."
        else:
            print "Error: %d pages in PDF file." % (document_page_count)
        return images

