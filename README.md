# TBudget2CSV
A tool to convert Thailand's national budget PDF to machine readable CSV format.

## Getting start
- Use Python3
- Install pdf2text on Linux `sudo apt install python3-pdfminer`

## Usage
- Download budget PSF file from http://www.bb.go.th/topic3.php?gid=860&mid=544 filename "ร่างพระราชบัญญัติงบประมาณรายจ่ายประจำปีงบประมาณ พ.ศ. 2565" and save it to `budget2022.pdf`.
- Run the python file `python3 tbudget2csv.py budget2022.pdf`. The output will be `budget2022.csv`

## Result
https://docs.google.com/spreadsheets/d/1qhHmQnWPDDfFeN8tTNW4uzg1E1NEDGPOjeJ2CfSFSTU/edit?usp=sharing
