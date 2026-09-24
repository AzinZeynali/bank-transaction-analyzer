# Bank Transaction Analyzer

A desktop GUI tool (Python + Tkinter) for analyzing bank transaction Excel exports — filter by date and document number, and flag documents with mismatched action codes.

## Features
- Load an Excel file (.xlsx/.xls) exported from a bank system
- Select a date from a dropdown, then a document number
- View all transaction rows for that document
- Automatically flags documents where rows have different "کد عمل" (action code) values

## Tech Stack
- Python
- pandas (data processing)
- Tkinter (GUI)

## How to Run

pip install -r requirements.txt
python bank_analyzer.py


## About
Built as a personal project to practice data processing and GUI development in Python.