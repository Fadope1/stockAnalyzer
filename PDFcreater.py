from fpdf import Template
import PyPDF2
import os

created_pages = []

front_page = [
    { 'name': 'stock_name', 'type': 'T', 'x1': 0.0, 'y1': 0.0, \
    'x2': 200.0, 'y2': 25.0, 'font': 'Arial', 'size': 20.0, 'bold': 2, \
    'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, \
    'align': 'C', 'text': '', 'priority': 3, },
    { 'name': 'stock_front_image', 'type': 'I', 'x1': 30.0, 'y1': 30.0, \
    'x2': 150.0, 'y2': 100.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'image', 'priority': 2, },
    { 'name': 'analytics', 'type': 'T', 'x1': 50.0, 'y1': 50, \
    'x2': 200.0, 'y2': 200.0, 'font': 'Arial', 'size': 15.0, 'bold': 2, \
    'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, \
    'align': 'C', 'text': '', 'priority': 10, },
]

landscape = [
    { 'name': 'interval', 'type': 'T', 'x1': 0.0, 'y1': 0.0, \
    'x2': 200.0, 'y2': 25.0, 'font': 'Arial', 'size': 20.0, 'bold': 2, \
    'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, \
    'align': 'C', 'text': '', 'priority': 3, },
    { 'name': '0', 'type': 'I', 'x1': 30.0, 'y1': 30.0, \
    'x2': 150.0, 'y2': 100.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'logo', 'priority': 2, },
    { 'name': '1', 'type': 'I', 'x1': 30.0, 'y1': 30.0, \
    'x2': 150.0, 'y2': 100.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'logo', 'priority': 2, },
    { 'name': '2', 'type': 'I', 'x1': 30.0, 'y1': 30.0, \
    'x2': 150.0, 'y2': 100.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'logo', 'priority': 2, },
    { 'name': '3', 'type': 'I', 'x1': 30.0, 'y1': 30.0, \
    'x2': 150.0, 'y2': 100.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'logo', 'priority': 2, },
] # quer format

portrait = [
    { 'name': 'interval', 'type': 'T', 'x1': 0.0, 'y1': 0.0, \
    'x2': 200.0, 'y2': 25.0, 'font': 'Arial', 'size': 0.0, 'bold': 2, \
    'italic': 0, 'underline': 1, 'foreground': 0, 'background': 0, \
    'align': 'C', 'text': '', 'priority': 3, },
    { 'name': '0', 'type': 'I', 'x1': 10.0, 'y1': 10.0, \
    'x2': 200.0, 'y2': 75.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'first_pic', 'priority': 2, },
    { 'name': '1', 'type': 'I', 'x1': 10.0, 'y1': 80.0, \
    'x2': 200.0, 'y2': 150.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'sec_pic', 'priority': 3, },
    { 'name': '2', 'type': 'I', 'x1': 10.0, 'y1': 150.0, \
    'x2': 200.0, 'y2': 225.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'third_pic', 'priority': 3, },
    { 'name': '3', 'type': 'I', 'x1': 10.0, 'y1': 220.0, \
    'x2': 200.0, 'y2': 300.0, 'font': None, 'size': 0.0, 'bold': 0, 'italic': 0, \
    'underline': 0, 'foreground': 0, 'background': 0, 'align': 'I', \
    'text': 'thourth_pic', 'priority': 3, },
] # normales format

def chartPages(stock_name:"str", interval:"str", indicators:"list", page_num=0) -> "temp. PDF file":
    # add indicator for every diagram?

    chartPage = Template(format="A4", elements=portrait, title=f"{interval}diagrams") # chagen elements by argument? -> compile/ s-/getattr?
    chartPage.add_page()

    chartPage["interval"] = f"Interval: {interval}" # interval as title for every page

    # this will create a page filled with diagrams using the interval and with different Indicators
    indicator_remaining = indicators.copy()
    for i, indicator in enumerate(indicators):
        if i == 4:
            chartPages(stock_name, interval, indicator_remaining, page_num=page_num+1) # recursion to create as many pdf as needed
            break
        chartPage[str(i)] = f'./.tempPictures/{stock_name}{interval}{indicator}.png' # create all diagrams
        indicator_remaining.remove(indicator)

    for n in range(i+1, 4):
        chartPage[str(n)] = None

    render_path = f"./{stock_name}{interval}{page_num}.pdf"
    chartPage.render(render_path)
    created_pages.append(render_path)

def createPDF(stock_name, intervals, indicators, stock_data:"analytics"=None, stock_news:"news" = None) -> "PDF file":
    # create the first page of the PDF -> front page
    page = Template(format="A4", elements=front_page,
                 title="Front page")

    page.add_page()

    page["stock_name"] = stock_name
    for interval in intervals:
        try:
            page["stock_front_image"] = f"./.tempPictures/{stock_name}{interval}.png"
            break
        except:
            intervals.remove(interval)
            continue
    # print(stock_data) # extract what is usefull and then display -> currently none, bc not working duh
    # page["analytics"] = stock_data
    page["analytics"] = "THIS IS A RANDOM TEXT BECAUSE I DONT HAVE LOREM IPSUM INSTALLED AND I DONT WANNA GOOGLE THIS LOOOOL"

    page.render(f"./{stock_name}analytics.pdf") #, dest="S") # add the current date to output name???

    # create rest pages for all intervals and indicators
    for interval in intervals:
        chartPages(stock_name, interval, indicators)

    # create the final PDF
    pdfWriter = PyPDF2.PdfFileWriter()
    # Add the first page -> the analytics/ news
    analytics_file_name = f"{stock_name}analytics.pdf"
    # print(analytics_file_name)
    first_page = open(analytics_file_name, "rb")
    pdfReader = PyPDF2.PdfFileReader(first_page)
    pdfWriter.addPage(pdfReader.getPage(0))
    os.remove(analytics_file_name)

    # add the rest of the pages -> stock diagram in the intervals with different indicators
    # stock_name, intervals, indicators
    for page in created_pages[::-1]:
        # print(page)
        rest_pages = open(page, "rb")
        pdfReader = PyPDF2.PdfFileReader(rest_pages)
        pdfWriter.addPage(pdfReader.getPage(0))
        os.remove(page)

    with open(f"{stock_name}_analysis.pdf", "wb") as file:
        pdfWriter.write(file)

    first_page.close()
    rest_pages.close()
