# Notes

- Assumptions about pdf format

  I have exracted the text from pdf file with pdf2text and then have assumed following things in order to parse the data
  
  1. First non empty row content is considered to be company name.
  2. There is a row that contains 'Particulars' word that separates the company info from balance sheet line items. After   'Particulars' every row may have line items.
  3. Then for every line item row, it can have zero or more columns.
  
- Parsing Algorithm

    1. Parsing logic is based on how many number are present of the format (123.00) in row. For now, I have considered two decimal places only. But it can be extended to a genralized format.
    2. Once, we determine how many numbers are present there can be three cases.
        * 0 numbers means empty line
        * 2 numbers means either left line item is present or right line item is present.
        * 4 numbers means both line items are present or it is a total row
            
            1. if a entry is present which start with `To Line Item` then there are line items in row. so extract each line item.
            2. If not, it is a total row then extract the patterns starting with `Total`.
            
  
