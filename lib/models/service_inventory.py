from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from lib.base import Base
from lib.models.inventory import Inventory
from lib.models.service import Service

class ServiceInventory(Base):
    __tablename__ = "service_inventory"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    quantity_used = Column(Integer, nullable=False)  
    created_at = Column(DateTime, default=datetime.utcnow)  # ✅ Store timestamp when linked
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Update timestamp when modified

    service = relationship("Service")
    inventory = relationship("Inventory")

    @classmethod
    def link_service_to_inventory(cls, db: Session, service_id: int, inventory_id: int, quantity_used: int):
        """Links a service to an inventory item and defines quantity used per service."""
        inventory_item = db.query(Inventory).filter(Inventory.id == inventory_id).first()

        if not inventory_item:
            raise ValueError("Inventory item not found!")

        if quantity_used <= 0:
            raise ValueError("Quantity used must be greater than zero!")

        if quantity_used > inventory_item.quantity:
            raise ValueError("Insufficient stock available!")

        service_inventory = cls(
            service_id=service_id, 
            inventory_id=inventory_id, 
            quantity_used=quantity_used, 
            created_at=datetime.utcnow
        )
        
        inventory_item.quantity -= quantity_used  # ✅ Deduct from inventory stock
        inventory_item.updated_at = datetime.utcnow  # ✅ Apply timestamp update

        db.add(service_inventory)
        db.commit()
        db.refresh(service_inventory)
        return {"message": "Service linked successfully!", "service_inventory": service_inventory}

    @classmethod
    def get_inventory_for_service(cls, db: Session, service_id: int):
        """Gets all inventory items linked to a service."""
        inventory_items = db.query(cls).filter(cls.service_id == service_id).all()
        if not inventory_items:
            raise ValueError("No inventory found for this service.")
        return inventory_items
