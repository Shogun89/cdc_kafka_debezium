from models import User, Product, Order, OrderItem, ProductCategory
from datetime import datetime, timezone


def process_user(db, operation, data):
    if operation in ("c", "u"):  
        user = User(
            id=data["id"],
            email=data["email"],
            is_active=bool(data["is_active"]),
            created_at=(
                datetime.fromtimestamp(data["created_at"] / 1000, timezone.utc)
                if data["created_at"]
                else None
            ),
            last_login=(
                datetime.fromtimestamp(data["last_login"] / 1000, timezone.utc)
                if data["last_login"]
                else None
            ),
        )
        db.merge(user)
    elif operation == "d":  
        user = db.query(User).filter(User.id == data["id"]).first()
        if user:
            db.delete(user)


def process_product(db, operation, data):
    if operation in ("c", "u"):
        product = Product(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            price=float(data["price"]),
            category_id=data["category_id"],
        )
        db.merge(product)
    elif operation == "d":
        product = db.query(Product).filter(Product.id == data["id"]).first()
        if product:
            db.delete(product)


def process_order(db, operation, data):
    if operation in ("c", "u"):
        order = Order(
            id=data["id"],
            user_id=data["user_id"],
            status=data["status"],
            created_at=(
                datetime.fromtimestamp(data["created_at"] / 1000, timezone.utc)
                if data["created_at"]
                else None
            ),
        )
        db.merge(order)
    elif operation == "d":
        order = db.query(Order).filter(Order.id == data["id"]).first()
        if order:
            db.delete(order)


def process_order_item(db, operation, data):
    if operation in ("c", "u"):
        order_item = OrderItem(
            id=data["id"],
            order_id=data["order_id"],
            product_id=data["product_id"],
            quantity=data["quantity"],
            price=data["price"],
        )
        db.merge(order_item)
    elif operation == "d":
        order_item = db.query(OrderItem).filter(OrderItem.id == data["id"]).first()
        if order_item:
            db.delete(order_item)


def process_product_category(db, operation, data):
    if operation in ("c", "u"):
        category = ProductCategory(id=data["id"], name=data["name"])
        db.merge(category)
    elif operation == "d":
        category = (
            db.query(ProductCategory).filter(ProductCategory.id == data["id"]).first()
        )
        if category:
            db.delete(category)


processors = {
    "users": process_user,
    "products": process_product,
    "orders": process_order,
    "order_items": process_order_item,
    "product_categories": process_product_category,
}
