__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from peewee import fn
from datetime import datetime

from models import Product, User, Tag, UserProduct, ProductTag, Transaction, Catalog


def search(term):
    return Product.select().where(
        fn.Lower(Product.product_name).contains(fn.Lower(term))
    )


def list_user_products(user_id):
    return (
        UserProduct.select(
            User.first_name,
            User.last_name,
            Product.product_name,
        )
        .join(UserProduct)
        .join(User)
        .where(UserProduct.user_id == user_id)
    )


def list_products_per_tag(tag_id):
    return (
        Tag.select(Product.product_name, Tag.name)
        .join(Product)
        .switch(Tag)
        .join(Tag)
        .where(UserProduct.user_id == tag_id)
    )


def add_product_to_catalog(user_id, product_name):

    product = Product.create(
        product_name=product_name,
        description="",
        price_per_unit=100.0,
        number_in_stock=1,
    )
    UserProduct.create(user_id=user_id, product_id=product)
    return product


# price # quantity


def update_stock(product_id, new_quantity):
    product = UserProduct.get(UserProduct.product_id == product_id)
    new_quantity = product.quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity, price):
    Transaction.create(
        user_id=buyer_id,
        product_id=product_id,
        number=quantity,
        sell_date=datetime.now(),
        sell_price=price,
    )


def remove_product(product_id):
    product = Product.get(UserProduct.product_id == product_id)
    product.delete_instance()


if __name__ == "__main__":
    result = search("airco")
    print(result)
