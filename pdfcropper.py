from PyPDF2 import PdfFileReader, PdfFileWriter
import os, sys, click

@click.command()
@click.option('--examref', is_flag=True)
@click.option('--packtpub', is_flag=True)
@click.option('--manning', is_flag=True)
@click.argument('filename')
def setmargins(examref, packtpub, manning, filename):
  oddLeft, oddTop, oddRight, oddBottom, evenLeft, evenTop, evenRight, evenBottom, top, right, bottom, left = 0,0,0,0,0,0,0,0,0,0,0,0
  if examref:
    top, right, bottom, left= 1.5,0,1.75,0
    oddLeft   =1.75
    oddTop    =top
    oddRight  =1.5
    oddBottom =bottom
    evenLeft  =1.5
    evenTop   =top
    evenRight =1.75
    evenBottom=bottom
  if packtpub:
    top, right, bottom, left = 0.625, 0.75, 0.625, 0.75
    oddLeft   =left
    oddTop    =top
    oddRight  =right
    oddBottom =bottom
    evenLeft  =left
    evenTop   =top
    evenRight =right
    evenBottom=bottom
  if manning:
    top, right, bottom, left = 0.375, 0.875,0.5,0.375
    oddLeft   =0.5
    oddTop    =top
    oddRight  =0.75
    oddBottom =bottom
    evenLeft  =left
    evenTop   =top
    evenRight =right
    evenBottom=bottom


  
  oddLeft   *=72
  oddTop    *=72
  oddRight  *=72
  oddBottom *=72
  evenLeft  *=72
  evenRight *=72
  evenTop   *=72
  evenBottom*=72

  path = os.path.dirname(filename)
  filename = os.path.basename(filename)
  fo=f'{path}/{filename}-cropped.pdf'
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

pagesToExclude = []

if __name__ == "__main__":
  setmargins()
