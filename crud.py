from sqlalchemy.orm import Session
import models
import schemas
from typing import Optional, List


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Get a product by ID.

    Args:
        db (Session): The database session.
        product_id (int): The product ID.

    Returns:
        Optional[models.Product]: The product, or None if not found.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(
    db: Session,
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    category_id: Optional[int] = None
) -> List[models.Product]:
    """
    Get all products.

    Args:
        db (Session): The database session.
        name (Optional[str], optional): The product name. Defaults to None.
        min_price (Optional[float], optional): The minimum price. Defaults to None.
        max_price (Optional[float], optional): The maximum price. Defaults to None.
        category_id (Optional[int], optional): The category ID. Defaults to None.

    Returns:
        List[models.Product]: A list of products.
    """
    query = db.query(models.Product)

    if name is not None:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    elif min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    elif max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    elif category_id is not None:
        query = query.filter(models.Product.category_id == category_id)

    return query.all()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """
    Create a product.

    Args:
        db (Session): The database session.
        product (schemas.ProductCreate): The product to create.

    Returns:
        models.Product: The created product.
    """
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate) -> Optional[models.Product]:
    """
    Update a product.

    Args:
        db (Session): The database session.
        product_id (int): The product ID.
        product (schemas.ProductUpdate): The product to update.

    Returns:
        Optional[models.Product]: The updated product, or None if not found.
    """
    db_product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    if db_product:
        for attr, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, attr, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Delete a product by ID.

    Args:
        db (Session): The database session.
        product_id (int): The product ID.

    Returns:
        Optional[models.Product]: The deleted product, or None if not found.
    """
    db_product = db.query(models.Product).filter(
        models.Product.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Get a category by ID.

    Args:
        db (Session): The database session.
        category_id (int): The category ID.

    Returns:
        Optional[models.Category]: The category, or None if not found.
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session) -> List[models.Category]:
    """
    Get all categories.

    Args:
        db (Session): The database session.

    Returns:
        List[models.Category]: A list of categories.
    """
    return db.query(models.Category).all()


def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    """
    Create a category.

    Args:
        db (Session): The database session.
        category (schemas.CategoryCreate): The category to create.

    Returns:
        models.Category: The created category.
    """
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


# The updated category, or None if not found.
def update_category(db: Session, category_id: int, category: schemas.CategoryUpdate) -> Optional[models.Category]:
    """
    Update a category.

    Args:
        db (Session): The database session.
        category_id (int): The category ID.
        category (schemas.CategoryUpdate): The category to update.

    Returns:
        Optional[models.Category]: The updated category, or None if not found.
    """
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
   
    if db_category:
        for attr, value in category.model_dump(exclude_unset=True).items():
            setattr(db_category, attr, value)
        db.commit()
        db.refresh(db_category)
    return db_category


# The deleted category, or None if not found.
def delete_category(db: Session, category_id: int) -> Optional[models.Category]:
    """
    Delete a category.

    Args:
        db (Session): The database session.
        category_id (int): The category ID.

    Returns:
        Optional[models.Category]: The deleted category, or None if not found.
    """
    db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if db_category:
        db.delete(db_category)
        db.commit()
    return db_category
