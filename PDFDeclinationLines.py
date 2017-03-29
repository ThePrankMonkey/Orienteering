import sys, os, math, PyPDF2, fpdf
from PIL import Image, ImageDraw


# Get Arguments (File, Declination)
# original_path        = sys.argv[0]
# declination          = sys.argv[1]
original_path        = r'C:\Users\User1\Documents\4752.pdf'
declination          = -11
watermark_image_path = r'C:\Temp\watermark.gif'
watermark_pdf_path   = r'C:\Temp\watermark.pdf'
declination_Rads     = -declination*(math.pi/180)
path_parts           = os.path.split(original_path)
output_path          = os.path.join(path_parts[0], path_parts[1].replace(".pdf", "_marked.pdf"))
print("The file that will be marked is called:", original_path)
print("The declination we are using is:       ", declination)


# Get dimensions of PDF
inputPDF = PyPDF2.PdfFileReader(open(original_path, 'rb'))
pageObj  = inputPDF.getPage(0)
width    = pageObj.mediaBox.getLowerRight_x()
height   = pageObj.mediaBox.getUpperLeft_y()
print("The dimensions of the input PDF is:    ", width, "x", height)


# Make GIF with lines at declination
im    = Image.new('RGBA', (width, height), (255, 255, 255, 0)) 
draw  = ImageDraw.Draw(im)
step  = int(height*math.atan(declination_Rads))
count = 0
while count < width:
    draw.line((count,0, step+count,height), fill=0, width=1)
    count += 50
count = 0
while step+count > 0:
    draw.line((count,0, step+count,height), fill=0, width=1)
    count -= 50
try:
    os.stat(os.path.dirname(watermark_image_path))
except:
    os.mkdir(os.path.dirname(watermark_image_path))     
im.save(watermark_image_path, 'GIF', transparency=0)


# Convert declination PNG to pdf
try:
    watermark = fpdf.FPDF()
    watermark.add_page()
    watermark.image(watermark_image_path)
    watermark.output(watermark_pdf_path, 'F')
    print("Declination GIF converted to PDF")
except:
    print("Error converting Declination GIF to PDF")


# Add declination PDF as watermark to original pdf
watermarkReader = open(watermark_pdf_path, 'rb')
pdfWatermarkReader = PyPDF2.PdfFileReader(watermarkReader)
pageObj.mergePage(pdfWatermarkReader.getPage(1))


# print Output
pdfWriter = PyPDF2.PdfFileWriter()
pdfWriter.addPage(pageObj)
resultPdfFile = open(output_path, 'wb')
pdfWriter.write(resultPdfFile)
print("Marked PDF successfully created at:    ", output_path)
resultPdfFile.close()
watermarkReader.close()


# remove temp filesys_decode
try:
    os.remove(watermark_image_path)
    print("Successfully removed:", watermark_image_path)
except:
    print("Unable to remove:    ", watermark_image_path)
try:
    os.remove(watermark_pdf_path)
    print("Successfully removed:", watermark_pdf_path)
except:
    print("Unable to remove:    ", watermark_pdf_path)
