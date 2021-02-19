import peewee

db = peewee.SqliteDatabase("betsy_workshop.db", pragmas={"foreign_keys": 1})


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    first_name = peewee.CharField()
    last_name = peewee.CharField()
    street = peewee.CharField()
    street_no = peewee.IntegerField()
    city = peewee.CharField()
    credit_card = peewee.IntegerField()


class Tag(BaseModel):
    name = peewee.CharField()


class Catalog(BaseModel):
    catalog_id = peewee.AutoField()
    user_id = peewee.ForeignKeyField(User)


class Product(BaseModel):
    product_name = peewee.CharField()
    description = peewee.CharField()
    tags = peewee.ManyToManyField(Tag)
    price = peewee.DecimalField()
    quantity = peewee.IntegerField()


class UserProduct(BaseModel):
    user_id = peewee.ForeignKeyField(User)
    product_id = peewee.ForeignKeyField(Product)
    number = peewee.IntegerField()


class Transaction(BaseModel):
    user_id = peewee.ForeignKeyField(User)
    product_id = peewee.ForeignKeyField(Product)
    quantity = peewee.IntegerField(constraints=[peewee.Check("quantity >= 0")])
    sell_date = peewee.DateField()
    sell_price = peewee.DecimalField()


ProductTag = Product.tags.get_through_model()


def create_tables():
    with db:
        db.create_tables(
            [User, Product, Tag, UserProduct, ProductTag, Transaction, Catalog]
        )


if __name__ == "__main__":
    create_tables()
