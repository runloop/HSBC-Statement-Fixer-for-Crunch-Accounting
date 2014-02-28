HSBC Statement Fixer for Crunch Accounting
==========================================

The combination of HSBC's poor statement downloads (why are all downloads named Transactions.csv?) and Crunch's poor CSV import functionality (everything else considers the CSV valid, why don't you?) makes life even more miserable when your accounts are due.

Up until recently we were able to fix the HSBC CSVs using this [online tool](http://digitalblahblah.com/crunch/). However, Crunch's import tool no longer imports the fixed CSVs either.

Here is a Python script you can run on your own computer* that will:

1. Search for all documents in a specified directory that looks like Transactions.csv / Transactions-1.csv etc

2. Fill in all the empty fields with correct data so that Crunch's CSV importer will consider it valid.

3. Save new files with meaningful names: transactions.20131212-20140109.csv for instance.

The result is a directory of CSV files that you can identify easily and that will import into Crunch without any issues.

Usage
=====

    python fixer.py --input-dir /Users/dan/Document/Statements --output-dir /Users/dan/Documents/Statements/Fixed

