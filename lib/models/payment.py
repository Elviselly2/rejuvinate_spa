from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import Session
from datetime import datetime
from lib.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)  # ✅ Auto-set timestamp
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # ✅ Track modifications

    @classmethod
    def process_payment(cls, db: Session, customer_id: int, appointment_id: int, amount: float):
        """Processes a payment and ensures the amount is valid."""
        if amount <= 0:
            raise ValueError("Payment amount must be greater than zero.")

        payment = cls(
            customer_id=customer_id,
            appointment_id=appointment_id,
            amount=amount,
            payment_date=datetime.utcnow
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        return {"message": "Payment processed successfully!", "payment": payment}

    @classmethod
    def get_payment_history(cls, db: Session, customer_id: int):
        """Retrieves payment history for a customer."""
        payments = db.query(cls).filter(cls.customer_id == customer_id).all()
        if not payments:
            raise ValueError("No payment history found for this customer.")
        return payments
