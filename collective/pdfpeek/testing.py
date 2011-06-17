from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting, FunctionalTesting


class PdfpeekFixture(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.pdfpeek
        self.loadZCML(package=collective.pdfpeek)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.pdfpeek:default')


PDFPEEK_FIXTURE = PdfpeekFixture()
PDFPEEK_INTEGRATION_TESTING = IntegrationTesting(bases=(PDFPEEK_FIXTURE,), name="pdfpeek:Integration")
PDFPEEK_FUNCTIONAL_TESTING = FunctionalTesting(bases=(PDFPEEK_FIXTURE,), name="pdfpeek:Functional")
