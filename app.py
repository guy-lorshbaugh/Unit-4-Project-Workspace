import csv
import re
import datetime

from peewee import *

inventory = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField(primary_key=True)
    # product_name field in inventory.db must be unique
    product_name = CharField(unique=True)
    product_quantity = IntegerField(default=0, unique=False)
    product_price = IntegerField(default=0, unique=False)
    date_updated = DateField(null=True)

    class Meta:
        database = inventory

def initialize():
    """Create the database and the table if they don't already exist."""
    inventory.connect()
    inventory.create_tables([Product], safe=True)

def build_table():
    """Cleans CSV data and enters it into the database."""
    with open('inventory.csv', newline='') as inventory:
        reader = csv.reader(inventory)
        columns = next(reader)
        for row in reader:
            trim = re.compile(r'[^\d]+')
            date = datetime.datetime.strptime(row[3], "%m/%d/%Y")
            try:
                Product.create(
                           product_name=row[0],
                           product_price=trim.sub('',row[1]),
                           product_quantity=int(row[2]),
                           date_updated=date
                )
            except IntegrityError:
                prev_date = Product.select().where(Product.product_name == row[0]).get()
                print(f"{prev_date}: {prev_date.product_name}")
                print("prev_date: ", prev_date.date_updated)
                print("     date: ", date.date())
                if prev_date.date_updated >= date.date():
                    pass
                else:
                    Product.update(
                        product_price=trim.sub('',row[1]),
                        product_quantity=int(row[2]),
                        date_updated=date
                    ).where(Product.product_name == row[0]).execute


if __name__ == "__main__":
    initialize()
    build_table()