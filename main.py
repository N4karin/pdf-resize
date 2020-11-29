import glob
import PyPDF2

# Parameters for output-files (in pixel)
mapPdfWidth = 150
mapPdfHeight = 100
previewPdfWidth = 550
previewPdfHeight = 125

# other global variables
pdfs = []
pdf_width = 0
pdf_height = 0
target_height = 0
previewType = ""


def readfiles():
    # read pdfs in same directory
    for file in glob.glob("*.pdf"):
        print('Found pdf: ' + file)
        pdfs.append(file)


def create_preview(pdf, name):
    pdf.cropBox.lowerLeft = (0, pdf_height - target_height)
    pdf.cropBox.upperRight = (pdf_width, pdf_height)
    pdf.mediaBox.lowerLeft = (0, pdf_height - target_height)
    pdf.mediaBox.upperRight = (pdf_width, pdf_height)

    if preview_type == "map":
        pdf.scaleTo(mapPdfWidth, mapPdfHeight)
    else:
        pdf.scaleTo(previewPdfWidth, previewPdfHeight)

    output = PyPDF2.PdfFileWriter()
    output.addPage(pdf)
    with open(name + '_' + preview_type + '.pdf', 'wb') as f:
        output.write(f)

    print('Successfully created preview of type ' + preview_type + ' for ' + name)


readfiles()
for pdf_name in pdfs:
    # read pdf and get dimensions
    currentPdfFile = open(pdf_name, 'rb')
    currentPdfReader = PyPDF2.PdfFileReader(currentPdfFile)
    pdfPage = currentPdfReader.getPage(0)
    pdf_width = pdfPage.mediaBox[2]
    pdf_height = pdfPage.mediaBox[3]

    # create preview pdf based on dimensions
    target_height = round((previewPdfHeight * pdf_width) / previewPdfWidth)
    preview_type = "preview"
    create_preview(pdfPage, pdf_name)

    # create map pdf based on dimensions
    # reload page from source to prevent loading already altered pdf
    currentPdfReader = PyPDF2.PdfFileReader(currentPdfFile)
    pdfPage = currentPdfReader.getPage(0)

    target_height = round(((2 / 3) * pdf_width))
    preview_type = "map"
    create_preview(pdfPage, pdf_name)

