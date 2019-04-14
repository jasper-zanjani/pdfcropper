from PyPDF2 import PdfFileReader, PdfFileWriter
import os,sys

if os.uname().sysname == 'Linux':
  path = os.path.expanduser('~/Downloads/')
else:
  path = "C:/Users/jaspe/Documents/Books and Courses/"
filename = sys.argv[1]
if not filename.endswith('.pdf'):
  filename+='.pdf'
fo=f'{path}{filename}-cropped.pdf'

# Margins in inches
# --All pages
top, right, bottom, left= 1, 1, 1, 1

# --Odd pages
oddLeft   =left
oddTop    =top
oddRight  =right
oddBottom =bottom
# --Even pages
evenLeft  =left
evenTop   =top
evenRight =right
evenBottom=bottom

# Convert inches to points
oddLeft   *=72
oddTop    *=72
oddRight  *=72
oddBottom *=72
evenLeft  *=72
evenRight *=72
evenTop   *=72
evenBottom*=72

# pagesToBreak = [18,  ]
pagesToExclude = []

if __name__ == "__main__":
  with open(f'{path}{filename}','rb') as r:
    global orig
    orig = PdfFileReader(r)
    pages = orig.getNumPages()
    pagesToPrint = pages

    
    
    out = PdfFileWriter()
    for i in range(pagesToPrint):
      p = orig.getPage(i)
      y=float(p.mediaBox.getUpperRight_y())
      x=float(p.mediaBox.getUpperRight_x())
      # print(x,y)
      if (i+1)%2==0: # even pages
        p.cropBox.lowerLeft=(evenLeft,evenBottom)
        p.cropBox.upperRight= (x-evenRight,y-evenTop)
      else:          # odd pages
        p.cropBox.lowerLeft=(oddLeft,oddBottom)
        p.cropBox.upperRight= (x-oddRight,y-oddTop)
      if i not in pagesToExclude:
        out.addPage(p)
      else:
        continue
    with open(fo, "wb") as outf:
      out.write(outf)
      print(f'PDF cropped to {fo}')
