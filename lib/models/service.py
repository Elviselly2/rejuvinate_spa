from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from lib.base import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # Track when the service is added
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Track modifications

    @classmethod
    def add_service(cls, db: Session, name: str, description: str, price: float):
        """Adds a new service."""
        if price <= 0:
            raise ValueError("Service price must be greater than zero.")

        service = cls(name=name, description=description, price=price, created_at=datetime.utcnow)
        db.add(service)
        db.commit()
        db.refresh(service)  # ✅ Ensure latest data is retrieved
        return {"message": "Service added successfully!", "service": service}

    @classmethod
    def list_services(cls, db: Session):
        """Lists all available services."""
        services = db.query(cls).all()
        if not services:
            raise ValueError("No services found.")
        return services

    @classmethod
    def update_price(cls, db: Session, service_id: int, price: float):
        """Updates the price of a service."""
        if price <= 0:
            raise ValueError("Service price must be greater than zero.")

        service = db.query(cls).filter(cls.id == service_id).first()
        if not service:
            raise ValueError("Service not found.")

        service.price = price
        service.updated_at = datetime.utcnow  # Apply timestamp update
        db.commit()
        db.refresh(service)  # Ensure updated timestamp is applied
        return {"message": "Service price updated successfully!", "service": service}
