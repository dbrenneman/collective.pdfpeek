"""Unit tests for the asyncronous job procesing queue"""
import unittest
import fnmatch
from os import listdir
from os.path import abspath, dirname
from plone.mocktestcase import MockTestCase
from collective.pdfpeek.transforms import convertPDFToImage


class TestTransform(MockTestCase):
    """
    Unit tests for the transformation of PDF files to images.
    """
    pdf_files = []

    for f in listdir(abspath(dirname(__file__))):
        if fnmatch.fnmatch(f, '*.pdf'):
            pdf_files.append(abspath(dirname(__file__)) + '/' + f)

    def test_convert_pdf(self):
        """
        """
        converter = convertPDFToImage()
        for pdf in self.pdf_files:
            image = converter.ghostscript_transform(open(pdf, mode='rb').read(), 1)
            self.assertTrue(image != '')
            self.assertTrue(image != None)
            self.assertTrue(type(image) == type(''))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
