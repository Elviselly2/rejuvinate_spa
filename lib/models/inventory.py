from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from lib.base import Base

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Store timestamp when product is added
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Update timestamp when modified

    @classmethod
    def add_product(cls, db: Session, product_name: str, quantity: int):
        """Adds a new inventory item."""
        product = cls(product_name=product_name, quantity=quantity, created_at=datetime.utcnow)
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    @classmethod
    def update_stock(cls, db: Session, product_id: int, quantity: int):
        """Updates inventory stock, ensuring the product exists."""
        product = db.query(cls).filter(cls.id == product_id).first()
        if not product:
            raise ValueError("Product not found.")

        if quantity < 0 and abs(quantity) > product.quantity:
            raise ValueError("Insufficient stock to remove!")

        product.quantity += quantity  # Adjust stock
        product.updated_at = datetime.utcnow  # Apply timestamp update
        db.commit()
        db.refresh(product)
        return {"message": "Stock updated successfully!", "product": product}
