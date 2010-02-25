"""Unit tests for the asyncronous job procesing queue"""
import unittest
from plone.mocktestcase import MockTestCase


class TestAsync(MockTestCase):
    """
    """

    def test_queue(self):
        """

        Arguments:
        - `self`:
        """
        pass

    def test_job(self):
        """Test the job class

        Arguments:
        - `self`:
        """
        pass


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
