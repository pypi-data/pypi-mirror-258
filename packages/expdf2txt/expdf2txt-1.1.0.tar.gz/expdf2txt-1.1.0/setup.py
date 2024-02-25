from setuptools import setup, find_packages
import pathlib
setup(
    name="expdf2txt",
    version="1.1.0",
    description="PDF to TXT",
    long_description=pathlib.Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    author="Gaurav Mehra",
    author_email="gauravmehra930@gmail.com",
    install_requires=[
        'openai',
        'pytesseract',
        'PyPDF2',
        'PyMuPDF',
        ],
    keywords=['pdf2txt','pdftotxt','invoice2text','invoice2txt','ag tech','gaurav mehra','expdf2txt','pdftoimage','pdf2image'],
    packages=find_packages(),
    project_urls={
        "Source":"https://github.com/AgTech930/expdftotxt"
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
    ]
    )
