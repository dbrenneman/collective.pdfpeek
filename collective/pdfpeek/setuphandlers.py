##########################################################################
#                                                                        #
#        copyright (c) 2009 David Brenneman                              #
#        open-source under the GPL v2.1 (see LICENSE.txt)                #
#                                                                        #
##########################################################################

from collective.pdfpeek.browser.pdf import PDFPeekConfiguration
from collective.pdfpeek.interfaces import IPDFPeekConfiguration

def importVarious(context):
    """Miscellanous steps import handle
    """
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('collective.pdfpeek_various.txt') is None:
        return
    
    # Add additional setup code here
    portal = context.getSite()
    sm = portal.getSiteManager()

    if not sm.queryUtility(IPDFPeekConfiguration, name='pdfpeek_config'):
        sm.registerUtility(PDFPeekConfiguration(), IPDFPeekConfiguration, 'pdfpeek_config')

