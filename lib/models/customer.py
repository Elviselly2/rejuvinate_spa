from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from lib.base import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Auto-set timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def create(cls, db: Session, name: str, email: str, phone: str):
        """Creates a new customer."""
        customer = cls(name=name, email=email, phone=phone)
        db.add(customer)
        db.commit()
        db.refresh(customer)  # ✅ Ensure latest data is retrieved
        return customer

    @classmethod
    def get_by_email(cls, db: Session, email: str):
        """Fetches a customer by email or returns an error if not found."""
        customer = db.query(cls).filter(cls.email == email).first()
        if not customer:
            raise ValueError("Customer with this email does not exist.")
        return customer

    @classmethod
    def update_info(cls, db: Session, customer_id: int, name: str = None, phone: str = None):
        """Updates customer details if found; otherwise, returns an error."""
        customer = db.query(cls).filter(cls.id == customer_id).first()
        if not customer:
            raise ValueError("Customer not found.")

        if name:
            customer.name = name
        if phone:
            customer.phone = phone

        customer.updated_at = datetime.utcnow  # ✅ Apply timestamp update
        db.commit()
        db.refresh(customer)  # ✅ Ensure updated timestamp is applied
        return {"message": "Customer updated successfully!", "customer": customer}
