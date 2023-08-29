# Imports
import argparse
import csv
from rich.console import Console
from rich.table import Table
import pandas
from datetime import date, timedelta, datetime

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.

today_date = None

# Function to update today's date and save it to a file
def update_today(new_date):
    today_date = new_date
    with open('today.txt', 'w+') as file:
        file.write(today_date.strftime('%Y-%m-%d'))

# Function to load today's date from a file
def load_today():
    try:
        with open('today.txt', 'r') as file:
            saved_date = file.read()
            return datetime.strptime(saved_date, '%Y-%m-%d').date()
    except (FileNotFoundError, ValueError):
        return date.today()

# Initialize the internal today's date
today_date = load_today()

# Load the last used product ID from the bought.csv file
def load_last_product_id_bought():
    try:
        with open('bought.csv', 'r') as file:
            reader = csv.reader(file)
            last_row = list(reader)[-1]
            return int(last_row[0]) + 1
    except (FileNotFoundError, IndexError):
        return 1  # Start with ID 1 if file is not found or empty

# Function to record a product purchase
def record_purchase(product_name, buy_price, expiration_date):
    product_id = load_last_product_id_bought()
    with open('bought.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([product_id, product_name.lower(), today_date.strftime('%Y-%m-%d'), buy_price, datetime.strptime(expiration_date, '%Y-%m-%d').date()])
        print('Product purchase recorded')

# Load the last used product ID from the sold.csv file
def load_last_product_id_sold():
    try:
        with open('sold.csv', 'r') as file:
            reader = csv.reader(file)
            last_row = list(reader)[-1]
            return int(last_row[0]) + 1
    except (FileNotFoundError, IndexError):
        return 1  # Start with ID 1 if file is not found or empty

# Check whether item is in stock    
def check_stock(product_name):
    try:
        with open('bought.csv', 'r') as file:
            reader_bought = csv.reader(file)
            stock_list = []
            for row in reader_bought:
                if product_name == row[1] and datetime.strptime(row[2], '%Y-%m-%d').date() <= today_date and datetime.strptime(row[4], '%Y-%m-%d').date() > today_date:
                    stock_list.append(int(row[0]))
            if stock_list == []:
                return False
            else:
                try:
                    with open('sold.csv', 'r') as file:
                        reader_sold = csv.reader(file)
                        sold = []
                        for row in reader_sold:
                            sold.append(row[2])
                        for i in stock_list:
                            if str(i) not in sold:
                                return i
                        return False
                except (FileNotFoundError, IndexError):
                    return stock_list[0]
    except (FileNotFoundError, IndexError):
        return False
    
# Function to record a product sale
def record_sale(product_name, sell_price):
    product_id = load_last_product_id_sold()
    bought_id = check_stock(product_name)
    if bought_id == False:
        print('Item not in stock')
    else:
        with open('sold.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([product_id, product_name.lower(), bought_id, today_date.strftime('%Y-%m-%d'), sell_price])
            print('Product sale recorded')

# Function to generate sold report
def generate_sold(request_date):
    sold_report = {}
    with open('sold.csv', 'r') as sold_file:
        reader_sold = csv.reader(sold_file)
        for row in reader_sold:
            if datetime.strptime(row[3], '%Y-%m-%d').date() <= request_date:
                product_name = row[1]
                sell_price = float(row[4])
                key = (product_name, sell_price)
                if key in sold_report:
                    sold_report[key] += 1
                else:
                    sold_report[key] = 1
    return sold_report

# Function to generate expired items report
def generate_expired(request_date):
    sold = []
    try: 
        with open('sold.csv', 'r') as sold_file:
            reader_sold = csv.reader(sold_file)
            for row in reader_sold:
                sold.append(row[2])
    except FileNotFoundError:
        sold = []
    expired_report = {}
    with open('bought.csv', 'r') as bought_file:
        reader_bought = csv.reader(bought_file)
        for row in reader_bought:
            if datetime.strptime(row[4], '%Y-%m-%d').date() <= request_date and row[0] not in sold:
                product_name = row[1]
                buy_price = float(row[3])
                expiration_date = datetime.strptime(row[4], '%Y-%m-%d').date()
                key = (product_name, buy_price, expiration_date)
                if key in expired_report:
                    expired_report[key] += 1
                else:
                    expired_report[key] = 1
    return expired_report

# Function to generate inventory report
def generate_inventory(request_date):
    sold = []
    try:
        with open('sold.csv', 'r') as sold_file:
            reader_sold = csv.reader(sold_file)
            for row in reader_sold:
                sold.append(row[2])
    except FileNotFoundError:
        sold = []
    inventory = {}
    in_stock = []
    with open('bought.csv', 'r') as bought_file:
        reader_bought = csv.reader(bought_file)
        for row in reader_bought:
            if row[0] not in sold and datetime.strptime(row[2], '%Y-%m-%d').date() <= request_date and datetime.strptime(row[4], '%Y-%m-%d').date() > request_date:
                in_stock.append(row)
        for row in in_stock:
            product_name = row[1]
            buy_price = float(row[3])
            expiration_date = datetime.strptime(row[4], '%Y-%m-%d').date()
            key = (product_name, buy_price, expiration_date)
            if key in inventory:
                inventory[key] += 1
            else:
                inventory[key] = 1
    return inventory

# Function to generate revenue and profit report
def generate_report(start_date, end_date):
    total_revenue = 0
    total_profit = 0
    with open('sold.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            sell_date = datetime.strptime(row[3], '%Y-%m-%d').date()
            if start_date <= sell_date <= end_date:
                total_revenue += float(row[4])
                bought_id = row[2]
                with open('bought.csv', 'r') as bought_file:
                    bought_reader = csv.reader(bought_file)
                    for bought_row in bought_reader:
                        if bought_row[0] == bought_id:
                            total_profit += float(row[4]) - float(bought_row[3])
                            break
    return total_revenue, total_profit

# Function to convert csv files to excel
def convert_to_excel_bought():
    read_file = pandas.read_csv('bought.csv', header=None)
    read_file.to_excel('bought.xlsx', index=False, header=['product id', 'product name', 'buy date', 'buy price', 'expiration date'])

def convert_to_excel_sold():
    read_file = pandas.read_csv('sold.csv', header=None)
    read_file.to_excel('sold.xlsx', index=False, header=['product id', 'product name', 'bought id', 'sell date', 'sell price'])
    
# Function to convert csv files to excel
def convert_to_csv_bought(file):
    read_file = pandas.read_excel(f'{file}')
    read_file.to_csv(f'bought.csv', index=False, header=None)

def convert_to_csv_sold(file):
    read_file = pandas.read_excel(f'{file}')
    read_file.to_csv(f'sold.csv', index=False, header=None)

def main():
    pass

# Command-line argument parsing
parser = argparse.ArgumentParser(description='Supermarket Inventory Management Tool')
parser.add_argument('--advance', type=int, help='Advance today\'s date by the specified number of days')
parser.add_argument('--buy', nargs=3, metavar=('NAME', 'PRICE', 'EXPIRATION_DATE'), help='Record a product purchase')
parser.add_argument('--sell', nargs=2, metavar=('NAME', 'SELL_PRICE'), help='Record a product sale')
parser.add_argument('--sold', nargs=1, metavar=('DATE'), help='Generate overview of sold or expired products until specified date')
parser.add_argument('--inventory', nargs=1, metavar=('DATE'), help='Generate inventory overview of specified date')
parser.add_argument('--report', nargs=2, metavar=('START_DATE', 'END_DATE'), help='Generate revenue and profit report in a certain period')
parser.add_argument('--exportfile', nargs=1, metavar=('NAME'), help='Convert csv file to excel file')
parser.add_argument('--importfile', nargs=2, metavar=('NAME', 'TYPE'), help='Convert excel file to csv file, please specify whether it\'s a bought or sold file')

args = parser.parse_args()

if args.advance:
    new_date = today_date + timedelta(days=args.advance)
    update_today(new_date)
    print(f'Today\'s date has been advanced to {new_date.strftime("%Y-%m-%d")}')
elif args.buy:
    record_purchase(args.buy[0], args.buy[1], args.buy[2])
elif args.sell:
    record_sale(args.sell[0], args.sell[1])
elif args.sold:
    request_date = datetime.strptime(args.sold[0], '%Y-%m-%d').date()
    try:
        sold = generate_sold(request_date)
        print(f'Items sold until {request_date}:')
        console = Console()
        table = Table(show_header=True, header_style='bold red')
        table.add_column('Product', style='bold')
        table.add_column('Quantity')
        table.add_column('Sell Price', justify='right')
        for (product_name, sell_price), quantity in sold.items():
            table.add_row(product_name, str(quantity), str(sell_price))
        console.print(table)
    except FileNotFoundError:
        print('No items sold yet')
    try:
        expired = generate_expired(request_date)
        print((f'Items expired until {request_date}:'))
        console = Console()
        table = Table(show_header=True, header_style='bold red')
        table.add_column('Product', style='bold')
        table.add_column('Quantity')
        table.add_column('Buy Price', justify='right')
        table.add_column('Expiration Date')
        for (product_name, buy_price, expiration_date), quantity in expired.items():
            table.add_row(product_name, str(quantity), str(buy_price), str(expiration_date))
        console.print(table)
    except FileNotFoundError:
        print('No items expired yet')
elif args.inventory:
    request_date = datetime.strptime(args.inventory[0], '%Y-%m-%d').date()
    try:
        inventory = generate_inventory(request_date)
        print(f"\nInventory on {request_date}:")
        console = Console()
        table = Table(show_header=True, header_style='bold red')
        table.add_column('Product', style='bold')
        table.add_column('Quantity')
        table.add_column('Buy Price', justify='right')
        table.add_column('Expiration Date')
        for (product_name, buy_price, expiration_date), quantity in inventory.items():
            table.add_row(product_name, str(quantity), str(buy_price), str(expiration_date.strftime('%Y-%m-%d')))
        console.print(table)
    except FileNotFoundError:
        print('No items bought yet')
elif args.report:
    start_date = datetime.strptime(args.report[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(args.report[1], '%Y-%m-%d').date()
    try:
        revenue, profit = generate_report(start_date, end_date)
        print(f'From {start_date} till {end_date} a revenue of {revenue} and a profit of {profit} was made')
    except FileNotFoundError:
        print('No items sold yet')
elif args.exportfile:
    if args.exportfile[0] == 'bought': 
        convert_to_excel_bought()
    elif args.exportfile[0] == 'sold': 
        convert_to_excel_sold()
    else:
        print('File does not exist')
elif args.importfile:
    file = args.importfile[0]
    if args.importfile[1] == 'bought':
        convert_to_csv_bought(file)
    elif args.importfile[1] == 'sold':
        convert_to_csv_sold(file)
    else:
        print('Please specify whether this file is a bought or sold file')
else:
    print('No valid command provided. Use --help for usage instructions.')

if __name__ == "__main__":
    main()
