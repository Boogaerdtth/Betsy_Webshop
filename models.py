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

    # example_user_data = [
    #     ["Zeg-eens", "A", "A-straat", 15, "A-Town", 4563],
    #     ["Ali", "B", "B-straat", 16, "Birmingham", 4563],
    #     ["Mel", "C", "C-level", 17, "Steven Cgaltown", 4563],
    # ]

    # product_data = [
    #     ["Airco", "Verkoeling", 100, 3],
    #     ["Tuinschep", "Om plantjes te planten", 2.5, 100],
    #     ["Barbeque", "De leven", 80, 15],
    # ]

    # tag_data = [["tag 1"], ["tag 2"], ["tag 3"]]

    # user_product_data = [[1, 1], [1, 2], [2, 2]]

    # transaction_data = [[1, 1, 5], [1, 2, 6], [2, 3, 4]]

    # product_tag_data = [[1, 1], [2, 1], [3, 3]]

    # for item in product_data:
    #     Product.create(
    #         name=item[0], description=item[1], price=item[2], quantity=item[3]
    #     )

    # for item in example_user_data:
    #     User.create(
    #         first_name=item[0],
    #         last_name=item[1],
    #         street=item[2],
    #         street_no=item[3],
    #         city=item[4],
    #         credit_card=item[5],
    #     )

    # for item in tag_data:
    #     Tag.create(name=item[0])

    # for item in transaction_data:
    #     Transaction.create(user_id=item[0], product_id=item[1], quantity=item[2])

    # for item in user_product_data:
    #     UserProduct.create(user_id=item[0], product_id=item[1])

    # for item in product_tag_data:
    #     ProductTag.create(product_id=item[0], tag_id=item[1])


if __name__ == "__main__":
    create_tables()
