**Unique Product ID:**
The program automatically assigns an unique product ID to bought products via checking the ID of the last row with `last_row = list(reader)[-1]` and incrementing this ID with 1 by `return int(last_row[0]) + 1`. If it is the first product that's bought, the program will automatically give this product ID number 1 by a `try:, except (FileNotFoundError, IndexError)` combination. The unique ID is also copied to the 'sold' products list. This makes it possible to check whether any product is still in stock, that is whether this product is not sold yet. First of all, this is necessary for selling products, so that a product is not sold twice. Furthermore, it's necessary to create an inventory report of products on a given date.

**Checking whether item is in stock:**
The program checks whether an item is in stock by looping over unique product ID's in the bought file and checking whether these are in a list of product ID's extracted from the sold file. First the program makes a list of all product ID's in the sold file by
```
sold = []
for row in reader_sold:
	sold.append(row[2])
```
Then it will loop over the products in the bought files, check whether they are in the sold list and return it's product ID if it's not sold yet by
```
for i in stock_list:
	if str(i) not in sold:
		return i
```                  
**Error message when no items sold, bought or expired yet:**
When CLI commands `--sold`, `--inventory` and `--report` would be used when there were no buys and/or sells yet, the progam gives an error message that no items were bought or sold yet. It does this via a `try:, except FileNotFoundError` combination. Since in this case there is no bought/sold.csv file yet, the function gives a FileNotFound error and skips to `print('No items bought/sold yet').
