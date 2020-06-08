from PyPDF2 import PdfFileReader, PdfFileWriter
import os, sys, click

pagesToExclude = []

def crop(p, top, right, bottom, left):
  height = float(p.mediaBox.getUpperRight_y())
  width = float(p.mediaBox.getUpperRight_x())
  p.cropBox.upperLeft=(left, height - bottom)
  p.cropBox.lowerRight= (width - right, bottom)
  return p


@click.command()
@click.option('--format', type=click.Choice(['examref','packtpub','manning','nostarch'], case_sensitive=False))
@click.argument('filename')
def setmargins(format, filename):
  oddLeft, oddTop, oddRight, oddBottom, evenLeft, evenTop, evenRight, evenBottom, top, right, bottom, left = 0,0,0,0,0,0,0,0,0,0,0,0
  if format.lower()=='examref':
    top, right, bottom, left= 1.5,0,1.75,0
    oddLeft   =1.75
    oddTop    =top
    oddRight  =1.5
    oddBottom =bottom
    evenLeft  =1.5
    evenTop   =top
    evenRight =1.75
    evenBottom=bottom
  elif format.lower()=='packtpub':
    top, right, bottom, left = 0.625, 0.75, 0.625, 0.75
    oddLeft   =left
    oddTop    =top
    oddRight  =right
    oddBottom =bottom
    evenLeft  =left
    evenTop   =top
    evenRight =right
    evenBottom=bottom
  elif format.lower()=='manning':
    top, right, bottom, left = 0.375, 0.875,0.5,0.375
    oddLeft   =0.5
    oddTop    =top
    oddRight  =0.75
    oddBottom =bottom
    evenLeft  =left
    evenTop   =top
    evenRight =right
    evenBottom=bottom
  elif format.lower()=='nostarch':
    top, right, bottom, left= 0.5,0.625,0.25,0.625
    oddLeft,oddTop,oddRight,oddBotom,evenLeft,evenTop,evenRight,evenBottom = left,top,right,bottom,left,top,right,bottom
  else:
    oddLeft, oddTop, oddRight, oddBottom, evenLeft, evenTop, evenRight, evenBottom = top, right, bottom, left, top, right, bottom, left
  oddLeft   *=72
  oddTop    *=72
  oddRight  *=72
  oddBottom *=72
  evenLeft  *=72
  evenRight *=72
  evenTop   *=72
  evenBottom*=72

  # Read file
  # Might want to break this out into its own function, if I can figure out how to get the thing working outside of the `with` block!
  path = os.path.dirname(filename)
  filename = os.path.basename(filename)
  fo=f'{path}/{filename}-cropped.pdf'
  with open(f'{path}/{filename}','rb') as r:
    global orig
    orig = PdfFileReader(r)
    pagesToPrint = orig.getNumPages()
    
    out = PdfFileWriter()
    for i in range(pagesToPrint):
      if i not in pagesToExclude:
        p = orig.getPage(i)
        newpage = p
        if (i+1)%2==0: # even pages
          newpage = crop(p,evenTop,evenRight,evenBottom,evenLeft)
        else:          # odd pages
          newpage = crop(p, oddTop, oddRight, oddBottom, oddLeft)
        out.addPage(newpage)
      else:
        continue

    # Write file
    # Might need to break this out into its own function
    # def write_file(filename):
    with open(fo, "wb") as outf:
      out.write(outf)
      print(f'PDF cropped to {fo}')


if __name__ == "__main__":
  setmargins()

