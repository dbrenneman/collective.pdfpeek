Introduction
============

A Plone product that generates image thumbnail previews of PDF files uploaded
to Archetypes based content objects.

This product, when installed in a Plone 3.x site, will automatically generate 
preview and thumbnail images of each page of uploaded PDF files and store 
them annotated onto the content object containing the pdf file.

Requires GNU ghostscript, PyPDF and PIL!

The image generation currently takes place on object modified events.
I am working on an implementation with a clock server process.
This way the user does not have to wait for the images to be generated.

- Code repository: https://svn.plone.org/svn/collective/collective.pdfpeek
- Questions and comments to db@davidbrenneman.com
- Report bugs to db@davidbrenneman.com
