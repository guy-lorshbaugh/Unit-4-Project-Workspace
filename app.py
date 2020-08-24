import csv
import re
import datetime

from peewee import *

inventory = SqliteDatabase('inventory.db')


class Product(Model):
    product_id = AutoField(primary_key=True)
    product_name = CharField(max_length=255, unique=False)
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
    with open('inventory.csv', newline='') as inventory:
        reader = csv.reader(inventory)
        columns = next(reader)
        for row in reader:
            trim = re.compile(r'[^\d]+')
            Product.create(product_name=row[0],
                           product_price=trim.sub('',row[1]),
                           product_quantity=int(row[2]),
                           date_updated=datetime.datetime.strptime(row[3], "%m/%d/%Y")
            )


if __name__ == "__main__":
    initialize()
    build_table()

