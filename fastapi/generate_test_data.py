import requests
import random
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = "http://app:8000/api"  

def generate_user():
    return {
        "email": f"user{random.randint(1, 10000)}@example.com",
        "is_active": True
    }

def generate_product():
    return {
        "name": f"Product {random.randint(1, 1000)}",
        "description": f"This is a description for product {random.randint(1, 1000)}",
        "price": round(random.uniform(10.0, 1000.0), 2),
        "category_id": random.randint(1, 5) 
    }

def generate_order(user_id):
    return {
        "user_id": user_id,
        "total_amount": 0,  
        "status": "pending"
    }

def generate_order_item(order_id, product_id):
    return {
        "order_id": order_id,
        "product_id": product_id,
        "quantity": random.randint(1, 5),
        "price": 0  
    }

def create_user():
    user_data = generate_user()
    try:
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        response.raise_for_status()
        logging.info(f"Created user: {response.json()['email']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create user: {e}")
        logging.error(f"Response content: {response.text}")
        return None

def create_product():
    product_data = generate_product()
    try:
        response = requests.post(f"{BASE_URL}/products/", json=product_data)
        response.raise_for_status()
        logging.info(f"Created product: {response.json()['name']}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create product: {e}")
        logging.error(f"Response content: {response.text}")
        return None

def create_order(user_id):
    order_data = generate_order(user_id)
    try:
        response = requests.post(f"{BASE_URL}/users/{user_id}/orders", json=order_data)
        response.raise_for_status()
        logging.info(f"Created order for user {user_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create order: {e}")
        logging.error(f"Response content: {response.text}")
        return None

def create_order_item(order_id, product_id, product_price):
    order_item_data = generate_order_item(order_id, product_id)
    order_item_data["price"] = product_price
    try:
        response = requests.post(f"{BASE_URL}/order-items/", json=order_item_data)
        response.raise_for_status()
        logging.info(f"Created order item for order {order_id}, product {product_id}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to create order item: {e}")
        logging.error(f"Response content: {response.text}")
        return None

def create_orders_for_user(user, products):
    user_orders = 0
    user_order_items = 0
    for _ in range(random.randint(1, 3)):
        order = create_order(user["id"])
        if order:
            user_orders += 1
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                if create_order_item(order["id"], product["id"], product["price"]):
                    user_order_items += 1
    return user_orders, user_order_items

def create_product_categories():
    categories = ["Electronics", "Books", "Clothing", "Home & Garden", "Toys"]
    created_categories = []
    for category in categories:
        response = requests.post(f"{BASE_URL}/categories/", json={"name": category})
        if response.status_code == 200:
            created_category = response.json()
            created_categories.append(created_category)
            logger.info(f"Created category: {category}")
        else:
            logger.error(f"Failed to create category {category}: {response.status_code} {response.text}")
    return created_categories

def create_users(num_users=10):
    created_users = []
    for _ in range(num_users):
        user_data = {
            "email": f"user{random.randint(1000, 9999)}@example.com",
            "password": "password123"
        }
        response = requests.post(f"{BASE_URL}/users/", json=user_data)
        if response.status_code == 200:
            created_user = response.json()
            created_users.append(created_user)
            logger.info(f"Created user: {created_user['email']}")
        else:
            logger.error(f"Failed to create user: {response.status_code} {response.text}")
    logger.info(f"Created {len(created_users)} users")
    return created_users

def create_products(categories, num_products=20):
    created_products = []
    for _ in range(num_products):
        product = {
            "name": f"Product {random.randint(1000, 9999)}",
            "description": "A sample product",
            "price": round(random.uniform(10.0, 1000.0), 2),
            "category_id": random.choice(categories)['id']
        }
        response = requests.post(f"{BASE_URL}/products", json=product)
        if response.status_code == 200:
            created_product = response.json()
            created_products.append(created_product)
            logger.info(f"Created product: {created_product['name']}")
        else:
            logger.error(f"Failed to create product: {response.status_code} {response.text}")
    logger.info(f"Created {len(created_products)} products")
    return created_products

def main():
    logger.info("Starting test data generation")
    users = create_users()
    logger.info("Test data generation completed")

if __name__ == "__main__":
    main()
