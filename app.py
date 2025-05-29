from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from lib.config import SessionLocal, engine
from lib.base import Base
from lib.models.customer import Customer
from lib.models.service import Service
from lib.models.appointment import Appointment
from lib.models.payment import Payment
from lib.models.inventory import Inventory
from lib.models.service_inventory import ServiceInventory
from lib.models.appointment_inventory import AppointmentInventory
from datetime import datetime

# Initialize FastAPI app
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Rejuvenate Spa!"}

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- CUSTOMER ENDPOINTS ----------------------

@app.post("/customers/")
def create_customer(name: str, email: str, phone: str, db: Session = Depends(get_db)):
    customer = Customer(name=name, email=email, phone=phone)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@app.get("/customers/")
def list_customers(db: Session = Depends(get_db)):
    customers = db.query(Customer).all()
    return customers

@app.get("/customers/{email}")
def get_customer(email: str, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.email == email).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, name: str = None, phone: str = None, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    if name:
        customer.name = name
    if phone:
        customer.phone = phone
    db.commit()
    db.refresh(customer)
    return customer

@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}

# ---------------------- SERVICE ENDPOINTS ----------------------

@app.post("/services/")
def add_service(name: str, description: str, price: float, db: Session = Depends(get_db)):
    service = Service(name=name, description=description, price=price)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@app.get("/services/")
def list_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services

@app.put("/services/{service_id}")
def update_service(service_id: int, price: float, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service.price = price
    db.commit()
    db.refresh(service)
    return service

@app.delete("/services/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.id == service_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    db.delete(service)
    db.commit()
    return {"message": "Service deleted successfully"}

# ---------------------- APPOINTMENT ENDPOINTS ----------------------

@app.post("/appointments/")
def book_appointment(customer_id: int, service_id: int, staff_id: int, scheduled_time: datetime, db: Session = Depends(get_db)):
    appointment = Appointment(customer_id=customer_id, service_id=service_id, staff_id=staff_id, scheduled_time=scheduled_time)
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@app.get("/appointments/")
def list_appointments(db: Session = Depends(get_db)):
    appointments = db.query(Appointment).all()
    return appointments

@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment canceled successfully"}

# ---------------------- PAYMENT ENDPOINTS ----------------------

@app.post("/payments/")
def process_payment(customer_id: int, appointment_id: int, amount: float, db: Session = Depends(get_db)):
    payment = Payment(customer_id=customer_id, appointment_id=appointment_id, amount=amount)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

@app.get("/payments/")
def list_payments(db: Session = Depends(get_db)):
    payments = db.query(Payment).all()
    return payments

@app.delete("/payments/{payment_id}")
def refund_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record not found")
    
    db.delete(payment)
    db.commit()
    return {"message": "Payment refunded successfully"}

# ---------------------- INVENTORY ENDPOINTS ----------------------

@app.post("/inventory/")
def add_inventory_item(name: str, quantity: int, db: Session = Depends(get_db)):
    inventory = Inventory(name=name, quantity=quantity)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

@app.get("/inventory/")
def list_inventory(db: Session = Depends(get_db)):
    inventory = db.query(Inventory).all()
    return inventory

@app.put("/inventory/{product_id}")
def update_inventory_stock(product_id: int, quantity: int, db: Session = Depends(get_db)):
    inventory_item = db.query(Inventory).filter(Inventory.id == product_id).first()
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    inventory_item.quantity = quantity
    db.commit()
    db.refresh(inventory_item)
    return inventory_item

@app.get("/inventory/low-stock/")
def check_low_stock(db: Session = Depends(get_db)):
    low_stock_items = db.query(Inventory).filter(Inventory.quantity < 5).all()
    return low_stock_items
