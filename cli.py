import click
from sqlalchemy.orm import Session
from lib.config import SessionLocal
from lib.models.customer import Customer
from lib.models.service import Service
from lib.models.staff import Staff  
from lib.models.appointment import Appointment
from lib.models.payment import Payment
from lib.models.inventory import Inventory
from datetime import datetime

# Function implementations
def get_db():
    """Establish a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------------- CUSTOMER FUNCTIONS ----------------------

def add_customer(name, email, phone):
    """Add a new customer."""
    session = SessionLocal()
    customer = Customer(name=name, email=email, phone=phone)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    click.echo(f"✅ Customer {customer.name} added successfully!")
    session.close()

def get_customer(email):
    """Get customer details by email."""
    session = SessionLocal()
    customer = session.query(Customer).filter_by(email=email).first()
    session.close()
    if customer:
        click.echo(f"🔍 Customer: {customer.name}, Phone: {customer.phone}")
    else:
        click.echo("❌ Customer not found.")

def list_customers():
    """List all customers."""
    session = SessionLocal()
    customers = session.query(Customer).all()
    session.close()
    if customers:
        click.echo("\n📜 All Customers:")
        for customer in customers:
            click.echo(f"- {customer.name}, Email: {customer.email}, Phone: {customer.phone}")
    else:
        click.echo("❌ No customers found.")

# ---------------------- STAFF FUNCTIONS ----------------------

def list_staff():
    """List all staff members."""
    session = SessionLocal()
    staff_members = session.query(Staff).all()
    session.close()
    if staff_members:
        click.echo("\n👥 All Staff:")
        for staff in staff_members:
            click.echo(f"- {staff.name}, Role: {staff.role}")
    else:
        click.echo("❌ No staff found.")

# ---------------------- SERVICE FUNCTIONS ----------------------

def add_service(name, description, price):
    """Add a new spa service."""
    session = SessionLocal()
    service = Service(name=name, description=description, price=price)
    session.add(service)
    session.commit()
    session.refresh(service)
    click.echo(f"✅ Service {service.name} added successfully!")
    session.close()

def list_services():
    """List all spa services."""
    session = SessionLocal()
    services = session.query(Service).all()
    session.close()
    if services:
        click.echo("\n💆‍♀️ All Services:")
        for service in services:
            click.echo(f"- {service.name} - {service.description}: ${service.price}")
    else:
        click.echo("❌ No services found.")

# ---------------------- APPOINTMENT FUNCTIONS ----------------------

def book_appointment(customer_id, service_id, staff_id, scheduled_time):
    """Book a new appointment."""
    session = SessionLocal()
    appointment = Appointment(
        customer_id=customer_id,
        service_id=service_id,
        staff_id=staff_id,
        scheduled_time=datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")
    )
    session.add(appointment)
    session.commit()
    session.refresh(appointment)
    click.echo(f"✅ Appointment {appointment.id} scheduled for Customer {appointment.customer_id} at {appointment.scheduled_time}")
    session.close()

def get_appointments(customer_id):
    """List upcoming appointments for a customer."""
    session = SessionLocal()
    appointments = session.query(Appointment).filter_by(customer_id=customer_id).all()
    session.close()
    if appointments:
        for app in appointments:
            click.echo(f"📅 Appointment {app.id} on {app.scheduled_time}")
    else:
        click.echo("❌ No upcoming appointments found.")

# ---------------------- PAYMENT FUNCTIONS ----------------------

def process_payment(customer_id, appointment_id, amount):
    """Process a payment for an appointment."""
    session = SessionLocal()
    payment = Payment(customer_id=customer_id, appointment_id=appointment_id, amount=amount, status="Paid")
    session.add(payment)
    session.commit()
    session.refresh(payment)
    click.echo(f"💰 Payment of ${payment.amount} processed for Customer {payment.customer_id}")
    session.close()

# ---------------------- INVENTORY FUNCTIONS ----------------------

def add_inventory(product_name, quantity):
    """Add an inventory item."""
    session = SessionLocal()
    inventory_item = Inventory(product_name=product_name, quantity=quantity)
    session.add(inventory_item)
    session.commit()
    session.refresh(inventory_item)
    click.echo(f"✅ Inventory item {inventory_item.product_name} added with quantity {inventory_item.quantity}")
    session.close()

def update_inventory(product_id, quantity):
    """Update inventory stock quantity."""
    session = SessionLocal()
    inventory_item = session.query(Inventory).filter_by(id=product_id).first()
    if inventory_item:
        inventory_item.quantity = quantity
        session.commit()
        session.refresh(inventory_item)
        click.echo(f"🛠 Inventory updated: {inventory_item.product_name} now has {inventory_item.quantity} in stock")
    else:
        click.echo("❌ Inventory item not found.")
    session.close()

# ---------------------- MENU SYSTEM ----------------------

def display_menu():
    while True:
        click.echo("\n======== Rejuvenate Spa Management System ========")
        click.echo("1. Add Customer")
        click.echo("2. Get Customer")
        click.echo("3. Add Service")
        click.echo("4. List Services")
        click.echo("5. Book Appointment")
        click.echo("6. Get Appointments")
        click.echo("7. Process Payment")
        click.echo("8. Add Inventory")
        click.echo("9. Update Inventory Stock")
        click.echo("10. List Customers")  # 
        click.echo("11. List Staff")  # 
        click.echo("12. Exit")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            name = click.prompt("Enter customer name")
            email = click.prompt("Enter customer email")
            phone = click.prompt("Enter customer phone")
            add_customer(name, email, phone)
        elif choice == 2:
            email = click.prompt("Enter customer email")
            get_customer(email)
        elif choice == 3:
            name = click.prompt("Enter service name")
            description = click.prompt("Enter service description")
            price = click.prompt("Enter service price", type=float)
            add_service(name, description, price)
        elif choice == 4:
            list_services()
        elif choice == 5:
            customer_id = click.prompt("Enter customer ID", type=int)
            service_id = click.prompt("Enter service ID", type=int)
            staff_id = click.prompt("Enter staff ID", type=int)
            scheduled_time = click.prompt("Enter appointment date (YYYY-MM-DD HH:MM)")
            book_appointment(customer_id, service_id, staff_id, scheduled_time)
        elif choice == 6:
            customer_id = click.prompt("Enter customer ID", type=int)
            get_appointments(customer_id)
        elif choice == 7:
            customer_id = click.prompt("Enter customer ID", type=int)
            appointment_id = click.prompt("Enter appointment ID", type=int)
            amount = click.prompt("Enter payment amount", type=float)
            process_payment(customer_id, appointment_id, amount)
        elif choice == 8:
            product_name = click.prompt("Enter inventory item name")
            quantity = click.prompt("Enter quantity", type=int)
            add_inventory(product_name, quantity)
        elif choice == 9:
            product_id = click.prompt("Enter product ID", type=int)
            quantity = click.prompt("Enter new quantity", type=int)
            update_inventory(product_id, quantity)
        elif choice == 10:  
            list_customers()
        elif choice == 11:  
            list_staff()
        elif choice == 12:
            click.echo("✅ Exiting spa management system. Goodbye!")
            return
        else:
            click.echo("❌ Invalid choice, please try again.")

# Entry point
if __name__ == "__main__":
    display_menu()
