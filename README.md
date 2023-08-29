Supermarket Inventory Management Tool
This command-line tool helps you manage your supermarket's inventory by recording purchases and sales, generating reports, and import and export inventory overviews.

Usage:
python Supermarket.py [options]

Options:
	--advance DAYS: Advance program's internal date by a specified number of days.
	--buy NAME PRICE EXPIRATION_DATE: Record a product purchase with the given name, buy price, and expiration date.
	--sell NAME SELL_PRICE: Record a product sale with the given name and sell price.
	--sold DATE: Generate overview of sold and/or expired products until given date.
	--inventory DATE: Generate inventory overview of given date.
	--report START_DATE END_DATE: Generate a revenue and profit report for a given date range.
	--exportfile NAME: Convert csv file to excel file
	--importfile NAME: Convert excel file to csv file, please specify whether it's a bought or sold file

Examples:
Advancing the date:

	python Supermarket.py --advance 3
	This advances the current date by 3 days.

	python Supermarket.py --advance -2
	This turns back the current date by 2 days

Record a purchase:

	python Supermarket.py --buy banana 0.3 2023-09-15
	This records a purchase of a banana with a buy price of €0.30 and an expiration date of 15-09-2023.

Record a sale:

	python Supermarket.py --sell pineapple 2
	This records a sale of the product with a sell price of €2.00.

Generate a sold/expired report:

	python Supermarket.py --sold 2023-10-01
	This generates a report of all items sold and/or expired until 01-10-2023. This report includes the sell price and quantity of sold products and the buy price, quantity and expiration date of expired products.

Show inventory:

	python Supermarket.py --inventory 2023-08-28
	This displays the inventory of products in stock on 28-08-2023, including their quantities, buy prices, and expiration dates. Only products with the exact same name, buy price and expiration date will be counted as the same product. 

Generate a revenue and profit report:

	python Supermarket.py --report 2023-08-01 2023-09-01
	This generates a report for the revenue and profit between 01-08-2023 and 01-09-2023.

Export product csv to excel file:

	python Supermarket.py --exportfile bought
	This exports all bought products, including their buy date, buy price and expiration date to an excel file called 'bought.xlsx'.

	python Supermarket.py --exportfile sold
	This exports all sold products, including their bought id, sell date and sell price to an excel file called 'sold.xlsx'.

Import product excel file to csv:

	python Supermarket.py --importfile example.xlsx bought
	This imports an excel file to a bought.csv file. It overwrites any existing bought.csv files.

	python Supermarket.py --importfile sold
	This imports an excel file to a sold.csv file. It overwrites any existing sold.csv files.

Remember to keep the bought.csv, sold.csv, and today.txt files in the same directory as the script for proper functionality.
