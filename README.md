# XP-project

Webová aplikácia, ktorá umožňuje transformáciu nascanovanych faktúr do formy digitálnych dát pomocou OCR technológie. Výstupom by bol napríklad json, prípadne nejaký editovateľný dokument.

How to install OCR dependencies:

  1. Download and install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki
  2. pip install pytesseract
  3. pip install opencv-python
  4. Inside of python script specify path to Tesseract: "pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'"
