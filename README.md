# 2up
**2up** is a simple command-line utility that crops the margins around PDFs for the purpose of printing the pages as large as possible.

The script accepts a single argument (the PDF file to be cropped) and 2 optional arguments:
- `--packtpub` uses preset margins for use with PDFs from [PacktPub](packtpub.com)
- `--examref` uses preset margins for use with the "Exam Ref" series of Microsoft books.

```sh
python pdfcropper.py $PDF --packtpub
```
