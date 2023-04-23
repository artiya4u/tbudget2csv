# TBudget2CSV

A tool to convert Thailand's national budget PDF to machine readable CSV format.

## Getting start

- Use Python3 and `pdftotext` (A command to convert PDF to text)
- ON Ubuntu Linux, install `pdftotext` using `sudo apt install poppler-utils`
- On macOS, install `pdftotext` using `brew install poppler`
- On Windows, download `pdftotext` from https://blog.alivate.com.au/poppler-windows/ and add to PATH

## Usage

- Download budget PDF file from http://www.bb.go.th/topic3.php?gid=860&mid=544 filename "
  ร่างพระราชบัญญัติงบประมาณรายจ่ายประจำปีงบประมาณ พ.ศ. 2565" and save it to `budget-pdf-summary`.
- Run the python file `python3 tbudget2csv.py ./budget-pdf-summary/budget-2023.pdf`. The output will be `/budget-pdf-summary/budget-2023.csv`
- The red document, convert from a directory using `python3 tbudget2csv_red.py ./budget-pdf-red/`

## Result

https://docs.google.com/spreadsheets/d/1qhHmQnWPDDfFeN8tTNW4uzg1E1NEDGPOjeJ2CfSFSTU/edit?usp=sharing
