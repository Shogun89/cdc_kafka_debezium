from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime


def get_product_category(db: Session, category_id: int):
    """
    Retrieve a product category by its ID.

    Args:
        db (Session): The database session.
        category_id (int): The ID of the product category to retrieve.

    Returns:
        models.ProductCategory: The product category object if found, else None.
    """
    return (
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
        .first()
    )


def get_product_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of product categories.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.ProductCategory]: A list of product category objects.
    """
    return db.query(models.ProductCategory).offset(skip).limit(limit).all()


def create_product_category(db: Session, category: schemas.ProductCategoryCreate):
    """
    Create a new product category.

    Args:
        db (Session): The database session.
        category (schemas.ProductCategoryCreate): The product category data to create.

    Returns:
        models.ProductCategory: The created product category object.
    """
    db_category = models.ProductCategory(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_product(db: Session, product_id: int):
    """
    Retrieve a product by its ID.

    Args:
        db (Session): The database session.
        product_id (int): The ID of the product to retrieve.

    Returns:
        models.Product: The product object if found, else None.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of products.

    Args:
        db (Session): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.Product]: A list of product objects.
    """
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    """
    Create a new product.

    Args:
        db (Session): The database session.
        product (schemas.ProductCreate): The product data to create.

    Returns:
        models.Product: The created product object.
    """
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_user(db: Session, user_id: int):
    """
    Retrieve a user by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The ID of the user to retrieve.

    Returns:
        models.User: The user object if found, else None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by their email address.

    Args:
        db (Session): The database session.
        email (str): The email address of the user to retrieve.

    Returns:
        models.User: The user object if found, else None.
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of users with pagination.

    Args:
        db (Session): The database session.
        skip (int, optional): The number of users to skip. Defaults to 0.
        limit (int, optional): The maximum number of users to return. Defaults to 100.

    Returns:
        List[models.User]: A list of user objects.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (schemas.UserCreate): The user data to create.

    Returns:
        models.User: The created user object.

    """
    db_user = models.User(
        email=user.email, is_active=True, created_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
