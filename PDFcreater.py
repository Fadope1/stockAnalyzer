# this is basicly completly copied from the internet :D THANKS lol
from fpdf import Template
import PyPDF2
import os

elements = [
    { 'name': 'stock_name', 'type': 'T', 'x1': 17.0, 'y1': 32.5, \
    'x2': 115.0, 'y2': 37.5, 'font': 'Arial', 'size': 15.0, 'bold': 2, \
    'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, \
    'align': 'C', 'text': '', 'priority': 2, },
    { 'name': 'stock_front', 'type': 'I', 'x1': 20.0, 'y1': 17.0, \
    'x2': 78.0, 'y2': 30.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'logo', 'priority': 2, },
    { 'name': 'analytics', 'type': 'T', 'x1': 50.0, 'y1': 50, \
    'x2': 200.0, 'y2': 200.0, 'font': 'Arial', 'size': 15.0, 'bold': 2, \
    'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, \
    'align': 'C', 'text': '', 'priority': 10, },
]

def createPDF(stock_name, intervals, indicators, stock_data: "analytics"=None, stock_news: "news" = None) -> "Create a PDF file":
    # create the first page of the PDF
    #here we instantiate the template and define the HEADER
    page = Template(format="A4", elements=elements,
                 title="Sample Invoice")

    page.add_page()

    #we FILL some of the fields of the template with the information we want
    #note we access the elements treating the template instance as a "dict"
    page["stock_name"] = stock_name
    for interval in intervals:
        try:
            page["stock_front"] = f"./.tempPictures/{stock_name}{interval}.png"
            break
        except:
            continue
    print(stock_data) # extract what is usefull and then display -> currently none, bc not working duh
    page["analytics"] = stock_data

    #and now we render the page
    page.render(f"./{stock_name}analytics.pdf") #, dest="S") # add the current date to output name???

    # create every other pages


def OutdatetcreatePDF(stock_name, img_path, stock_data):
    #here we instantiate the template and define the HEADER
    page = Template(format="A4", elements=elements,
                 title="Sample Invoice")
    page2 = Template(format="A4", elements=elements,
                 title="Sample Invoice")

    page.add_page()
    page2.add_page()

    #we FILL some of the fields of the template with the information we want
    #note we access the elements treating the template instance as a "dict"
    page["company_name"] = stock_name
    page["company_logo"] = img_path
    page2["company_name"] = "test"
    page2["company_logo"] = img_path

    #and now we render the page
    page.render("./.page.pdf") #, dest="S")
    page2.render("./.page2.pdf") #, dest="S")

    # instead of saving and opening the pdfs, find a way not to :D -> stringio?

    # Open the files that have to be merged one by one
    pdf1File = open(".page.pdf", 'rb')
    pdf2File = open(".page2.pdf", 'rb')

    # Read the files that you have opened
    pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
    pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

    # Create a new PdfFileWriter object which represents a blank PDF document
    pdfWriter = PyPDF2.PdfFileWriter()

    # Loop through all the pagenumbers for the first document
    for pageNum in range(pdf1Reader.numPages):
        pageObj = pdf1Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Loop through all the pagenumbers for the second document
    for pageNum in range(pdf2Reader.numPages):
        pageObj = pdf2Reader.getPage(pageNum)
        pdfWriter.addPage(pageObj)

    # Now that you have copied all the pages in both the documents, write them into the a new document
    pdfOutputFile = open('MergedFiles.pdf', 'wb')
    pdfWriter.write(pdfOutputFile)

    # Close/ Remove all the files - Created as well as opened
    pdf1File.close()
    pdf2File.close()
    os.remove("./.page.pdf")
    os.remove("./.page2.pdf")
