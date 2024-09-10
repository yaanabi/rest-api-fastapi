from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from pydantic import BaseModel
from typing import List

class Base(DeclarativeBase):
    pass

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    products: Mapped[List["Product"]] = relationship(back_populates="category", cascade='all, delete-orphan')
    def __repr__(self):
        return f"Category {self.name}"

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name:Mapped[str] = mapped_column(nullable=False)
    description:Mapped[str] = mapped_column(nullable=True)
    price:Mapped[float] = mapped_column(Float)
    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"))

    category: Mapped["Category"] = relationship(back_populates="products")
