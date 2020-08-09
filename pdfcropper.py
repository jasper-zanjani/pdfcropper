
import click
pagesToExclude = []


class Margins():
    '''
    Container for page margins
    '''

    def __init__(
        self,
        top: float = 0,
        bottom: float = 0,
        left: float = 0,
        right: float = 0,

        evenTop: float = 0,
        evenBottom: float = 0,
        evenLeft: float = 0,
        evenRight: float = 0,

        oddTop: float = 0,
        oddBottom: float = 0,
        oddLeft: float = 0,
        oddRight: float = 0,
    ):

        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        self.evenTop = top if evenTop == 0 else evenTop
        self.evenBottom = bottom if evenBottom == 0 else evenBottom
        self.evenLeft = left if evenLeft == 0 else evenLeft
        self.evenRight = right if evenRight == 0 else evenRight

        self.oddTop = top if oddTop == 0 else oddTop
        self.oddBottom = bottom if oddBottom == 0 else oddBottom
        self.oddLeft = left if oddLeft == 0 else oddLeft
        self.oddRight = right if oddRight == 0 else oddRight

    def even(self, points=False):
        '''
        Return margins for even pages
        '''
        if points:
            output = {
                'top': self.evenTop * 72,
                'right': self.evenRight * 72,
                'bottom': self.evenBottom * 72,
                'left': self.evenLeft * 72
            }
        else:
            output = {
                'top': self.evenTop,
                'right': self.evenRight,
                'bottom': self.evenBottom,
                'left': self.evenLeft,
            }
        return output

    def odd(self, points=False):
        '''
        Return margins for odd pages
        '''
        if points:
            output = {
                'top': self.oddTop * 72,
                'right': self.oddRight * 72,
                'bottom': self.oddBottom * 72,
                'left': self.oddLeft * 72
            }
        else:
            output = {
                'top': self.oddTop,
                'right': self.oddRight,
                'bottom': self.oddBottom,
                'left': self.oddLeft,
            }
        return output


def crop(p, m):
    height = float(p.mediaBox.getUpperRight_y())
    width = float(p.mediaBox.getUpperRight_x())
    p.cropBox.upperLeft = (m['left'], height - m['top'])
    p.cropBox.lowerRight = (width - m['right'], m['bottom'])
    return p


def fileio(margins, filename):
    from PyPDF2 import PdfFileReader, PdfFileWriter
    import os
    import sys

    devnull = open(os.devnull, 'w')
    sys.stdout = devnull

    # Read file
    # Might want to break this out into its own function, if I can figure out
    # how to get the thing working outside of the `with` block!
    path = os.path.dirname(filename)
    filename = os.path.basename(filename)
    fo = f'{path}/{filename}-cropped.pdf'
    with open(f'{path}/{filename}', 'rb') as r:
        global orig
        orig = PdfFileReader(r, warndest=sys.stdout)
        pagesToPrint = orig.getNumPages()

        out = PdfFileWriter()
        for i in range(pagesToPrint):
            if i not in pagesToExclude:
                p = orig.getPage(i)
                newpage = p
                if (i + 1) % 2 == 0:  # even pages
                    m = margins.even(points=True)
                    newpage = crop(p, m)
                else:          # odd pages
                    m = margins.odd(points=True)
                    newpage = crop(p, m)
                out.addPage(newpage)
            else:
                continue

        # Write file
        # Might need to break this out into its own function
        # def write_file(filename):
        with open(fo, "wb") as outf:
            out.write(outf)
            print(f'PDF cropped to {fo}')


def getMargins(format, top=None, right=None, bottom=None, left=None):
    '''
    Return a Margins object containing margins suitable for cropping.
    '''
    if format.lower().startswith('e'):    # Examref
        output = Margins(
            top=1.3,
            bottom=1.75,
            oddLeft=1.75,
            evenRight=1.75,
            evenLeft=1.5,
            oddRight=1.5)
    elif format.lower().startswith('p'):  # PacktPub
        output = Margins(top=0.625, right=0.75, bottom=0.625, left=0.75)
    elif format.lower().startswith('m'):  # Manning
        output = Margins(
            top=0.375,
            right=0.875,
            bottom=0.5,
            left=0.375,
            oddLeft=0.5,
            oddRight=0.75)
    elif format.lower().startswith('n'):  # NoStarch
        output = Margins(top=0.5, right=0.625, bottom=0.25, left=0.625)
    elif format.lower().startswith('o'):  # O'Reilly
        output = Margins(top=0.625, right=0.75, bottom=0.5, left=0.75)

    if top is not None:
        print("Custom top dimension")
        output.top = top
        output.evenTop = top
        output.oddTop = top

    if bottom is not None:
        output.bottom = bottom
        output.evenBottom = bottom
        output.oddBottom = bottom

    if left is not None:
        output.left = left
        output.evenLeft = left
        output.oddLeft = left

    if right is not None:
        output.right = right
        output.evenRight = right
        output.oddRight = right

    # from tabulate import tabulate
    # print(tabulate(
    #   [
    #     ['Output margins:',f'output.top: {output.top}', output.right, output.bottom, output.left],
    #     ['Output even margins:',f'output.evenTop: {output.evenTop}', output.evenRight, output.evenBottom, output.evenLeft],
    #     ['Output even margins:',f'output.oddTop: {output.oddTop}', output.oddRight, output.oddBottom, output.oddLeft]
    #   ], headers=['', 'Top','Right','Bottom','Left']))

    # output.oddLeft   *=72
    # output.oddTop    *=72
    # output.oddRight  *=72
    # output.oddBottom *=72
    # output.evenLeft  *=72
    # output.evenRight *=72
    # output.evenTop   *=72
    # output.evenBottom*=72

    return output


@click.command()
@click.option('--top', type=float)
@click.option('--bottom', type=float)
@click.option('--left', type=float)
@click.option('--right', type=float)
@click.option('--format', type=click.Choice(
    ['examref', 'packtpub', 'manning', 'nostarch', 'oreilly'], case_sensitive=False))
@click.argument('filename')
def main(format, top, bottom, left, right, filename):
    margins = getMargins(format, top, right, bottom, left)

    # from tabulate import tabulate
    # print(tabulate(
    #   [
    #     ['Received margins:',f'margins.top: {margins.top}', margins.right, margins.bottom, margins.left],
    #     ['Received even margins:',f'margins.evenTop: {margins.evenTop}', margins.evenRight, margins.evenBottom, margins.evenLeft],
    #     ['Received even margins:',f'margins.oddTop: {margins.oddTop}', margins.oddRight, margins.oddBottom, margins.oddLeft]
    #   ], headers=['', 'Top','Right','Bottom','Left']))
    fileio(margins, filename)


if __name__ == "__main__":
    main()
