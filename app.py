from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jewellery.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ------------------- Customer Table -------------------
class Customer(db.Model):
    __tablename__ = "customers"

    customer_id = db.Column(db.String(30), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    registration_date = db.Column(db.Date, default=datetime.utcnow)
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")


# ------------------- Orders Table -------------------
class Order(db.Model):
    __tablename__ = "orders"

    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.String(30), db.ForeignKey("customers.customer_id"))
    order_date = db.Column(db.Date, default=datetime.utcnow)
    total_products = db.Column(db.Integer)
    total_amount = db.Column(db.Numeric(12, 2))
    paid_amount = db.Column(db.Numeric(12, 2))
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(50))
    customer = db.relationship("Customer", back_populates="orders")
    products = db.relationship("Product", back_populates="order", cascade="all, delete-orphan")


# ------------------- Products Table -------------------
class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"))
    product_name = db.Column(db.String(100))
    category = db.Column(db.String(50))
    carat = db.Column(db.String(10), nullable=True)
    weight = db.Column(db.Numeric(10, 2))
    rate = db.Column(db.Numeric(10, 2))
    making_charge = db.Column(db.Numeric(10, 2))
    amount = db.Column(db.Numeric(10, 2))
    order = db.relationship("Order", back_populates="products")


with app.app_context():
    db.create_all()


# ------------------- Helper -------------------
def customer_id_making(first_name, last_name, phone_number):
    date = datetime.utcnow().strftime("%Y%m%d")
    f = first_name[:2].upper()
    l = last_name[:2].upper()
    p = phone_number[-2:]
    return f"{f}{l}{date}{p}"


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/order", methods=["GET", "POST"])
def order():
    if request.method == "POST":
        # --- Customer Details ---
        first_name = (request.form.get("fname") or "").strip()
        last_name = (request.form.get("lname") or "").strip()
        address = (request.form.get("address") or "").strip()
        phone_number = (request.form.get("mobile_no") or "").strip()
        registration_date = datetime.utcnow().date()

        customer_id = customer_id_making(first_name, last_name, phone_number)

        customer = Customer.query.filter_by(customer_id=customer_id).first()
        if not customer:
            customer = Customer(
                customer_id=customer_id,
                first_name=first_name,
                last_name=last_name,
                address=address,
                phone_number=phone_number,
                registration_date=registration_date,
            )
            db.session.add(customer)

        # --- Order Details ---
        paid_amount = Decimal(request.form.get("paid_amount") or 0)
        payment_method = request.form.get("payment_mode")

        product_names = request.form.getlist("product_name")
        categories = request.form.getlist("category")
        carats = request.form.getlist("carat")
        weights = request.form.getlist("weight")
        rates = request.form.getlist("rate")
        making_charges = request.form.getlist("making_charge")
        amounts = request.form.getlist("amount")

        total = Decimal(0)
        products = []

        for i in range(len(product_names)):
            if product_names[i].strip():
                amt = Decimal(amounts[i] or 0)
                total += amt
                product = Product(
                    product_name=product_names[i],
                    category=categories[i],
                    carat=carats[i] if carats and carats[i] else None,
                    weight=Decimal(weights[i] or 0),
                    rate=Decimal(rates[i] or 0),
                    making_charge=Decimal(making_charges[i] or 0),
                    amount=amt,
                )
                products.append(product)

        payment_status = "Paid" if total == paid_amount else "Pending"

        order = Order(
            customer=customer,
            total_products=len(products),
            total_amount=total,
            paid_amount=paid_amount,
            payment_method=payment_method,
            payment_status=payment_status,
        )

        db.session.add(order)
        db.session.flush()  # get order_id

        for p in products:
            p.order_id = order.order_id
            db.session.add(p)

        db.session.commit()
        return redirect(url_for("order"))

    orders = Order.query.all()
    return render_template("order.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True)
