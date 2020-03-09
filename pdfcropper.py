from PyPDF2 import PdfFileReader, PdfFileWriter
import os,sys

path = os.path.dirname(sys.argv[1])
filename = os.path.basename(sys.argv[1])
fo=f'{path}/{filename}-cropped.pdf'

# Margins in inches
# --All pages
top, right, bottom, left= 1.125, 1.25, 1.25, 2.125

# --Odd pages
oddLeft   =2.0
oddTop    =top
oddRight  =1.5
oddBottom =bottom
# --Even pages
evenLeft  =2.375
evenTop   =top
evenRight =1.125
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

pagesToExclude = []

if __name__ == "__main__":
  with open(f'{path}/{filename}','rb') as r:
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
