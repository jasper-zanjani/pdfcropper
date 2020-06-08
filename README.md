# PDFCropper
**PDFCropper** is a simple command-line utility that crops the margins around PDFs for the purpose of printing as efficiently as possible.

The script accepts a single argument (the PDF file to be cropped) and a single option `--format`. 
The values passed to `--format` determine margins dimensions typical to that publisher: `examref` ("Exam Ref" series published by Microsoft), `manning`, `nostarch`, and `packtpub`. 
Support for custom margins coming soon...

#### Example
```sh
python pdfcropper.py ~/doc.pdf --format packtpub
```
