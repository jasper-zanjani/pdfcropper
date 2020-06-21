# PDFCropper
**PDFCropper** is a simple command-line utility (coded in Python) that crops the margins around PDFs for the purpose of printing as efficiently as possible.
It relies almost entirely on the venerable [PyPDF2](https://pypi.org/project/PyPDF2/) module.

The script accepts a single argument (the filename of the PDF file to be cropped) and a single option `--format`. 
The values passed to `--format` determine margin dimensions typical to that publisher:
- `examref` ("Exam Ref" series published by Microsoft)
- [`manning`](https://manning.com)
- [`nostarch`](https://nostarch.com)
- [`packtpub`](https://packtpub.com)

Alternatively, you can define custom margins in inches by supplying arguments to the following options:
- `--top`
- `--right`
- `--bottom`
- `--left`

```sh
python pdfcropper.py ~/doc.pdf --format packtpub --top 1.25
```

