from setuptools import setup, find_packages


version = '0.17'

setup(name='collective.pdfpeek',
      version=version,
      description="A Plone product that generates image thumbnail previews" +
      "of PDF files stored on ATCT based objects.",
      long_description=open("README.txt").read() + "\n" +
                       open("docs/INSTALL.txt").read() + "\n" +
                       open("docs/CHANGES.txt").read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Plone Zope Python PDF',
      author='David Brenneman',
      author_email='db@davidbrenneman.com',
      url='https://svn.plone.org/svn/collective/collective.pdfpeek',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.browserlayer',
          'pyPdf',
          'Products.PloneTestCase',
          'plone.mocktestcase>=1.0b3',
          ],
      extras_require = {
          'test': ['Products.PloneTestCase']
          },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )

