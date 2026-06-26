from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ----------------------------------------------------
# 1. Create Flask app
# ----------------------------------------------------
app = Flask(__name__)
app.config["SECRET_KEY"] = "beginner-secret-key"

# SQLite database file name: mudi_dokan.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mudi_dokan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create SQLAlchemy database object
db = SQLAlchemy(app)


# ----------------------------------------------------
# 2. Database tables / models
# ----------------------------------------------------
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    supplier = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(30), nullable=False)
    buy_price = db.Column(db.Float, nullable=False)
    sell_price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    low_stock_limit = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One product can have many sales
    sales = db.relationship("Sale", backref="product", lazy=True)

    def profit_per_unit(self):
        return self.sell_price - self.buy_price

    def stock_value(self):
        return self.sell_price * self.stock

    def is_low_stock(self):
        return self.stock <= self.low_stock_limit


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=True)
    quantity = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    profit = db.Column(db.Float, nullable=False)
    sale_date = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key connects Sale table with Product table
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)


# ----------------------------------------------------
# 3. Create database and add demo data
# ----------------------------------------------------
def create_demo_data():
    """This function adds some sample products when database is empty."""
    if Product.query.count() == 0:
        demo_products = [
            Product(
                name="Miniket Rice",
                category="Rice & Grains",
                supplier="Local Rice Supplier",
                unit="kg",
                buy_price=68,
                sell_price=75,
                stock=50,
                low_stock_limit=10,
            ),
            Product(
                name="Soybean Oil 1L",
                category="Oil",
                supplier="Fresh Distributor",
                unit="piece",
                buy_price=160,
                sell_price=175,
                stock=25,
                low_stock_limit=6,
            ),
            Product(
                name="Sugar",
                category="Grocery",
                supplier="City Wholesale",
                unit="kg",
                buy_price=125,
                sell_price=135,
                stock=40,
                low_stock_limit=8,
            ),
            Product(
                name="Lifebuoy Soap",
                category="Toiletries",
                supplier="Unilever Distributor",
                unit="piece",
                buy_price=38,
                sell_price=45,
                stock=5,
                low_stock_limit=5,
            ),
        ]

        db.session.add_all(demo_products)
        db.session.commit()


with app.app_context():
    db.create_all()
    create_demo_data()


# ----------------------------------------------------
# 4. Helper function for dashboard stats
# ----------------------------------------------------
def get_dashboard_stats():
    products = Product.query.all()
    sales = Sale.query.all()

    total_products = len(products)
    total_stock_value = sum(product.stock_value() for product in products)
    low_stock_count = sum(1 for product in products if product.is_low_stock())
    total_sales_amount = sum(sale.total_amount for sale in sales)
    total_profit = sum(sale.profit for sale in sales)

    return {
        "total_products": total_products,
        "total_stock_value": total_stock_value,
        "low_stock_count": low_stock_count,
        "total_sales_amount": total_sales_amount,
        "total_profit": total_profit,
    }


# ----------------------------------------------------
# 5. Website routes / pages
# ----------------------------------------------------
@app.route("/")
def home():
    search_name = request.args.get("name", "")
    search_category = request.args.get("category", "")
    stock_filter = request.args.get("stock", "")

    products = Product.query

    # Search by product name
    if search_name:
        products = products.filter(Product.name.ilike(f"%{search_name}%"))

    # Search by category
    if search_category:
        products = products.filter(Product.category.ilike(f"%{search_category}%"))

    products = products.order_by(Product.name.asc()).all()

    # Filter low stock after query
    if stock_filter == "low":
        products = [product for product in products if product.is_low_stock()]

    stats = get_dashboard_stats()

    return render_template(
        "index.html",
        products=products,
        stats=stats,
        search_name=search_name,
        search_category=search_category,
        stock_filter=stock_filter,
    )


@app.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("name")
        category = request.form.get("category")
        supplier = request.form.get("supplier")
        unit = request.form.get("unit")
        buy_price = float(request.form.get("buy_price"))
        sell_price = float(request.form.get("sell_price"))
        stock = int(request.form.get("stock"))
        low_stock_limit = int(request.form.get("low_stock_limit"))

        new_product = Product(
            name=name,
            category=category,
            supplier=supplier,
            unit=unit,
            buy_price=buy_price,
            sell_price=sell_price,
            stock=stock,
            low_stock_limit=low_stock_limit,
        )

        db.session.add(new_product)
        db.session.commit()

        flash("New product added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("add_product.html")


@app.route("/sell/<int:product_id>", methods=["GET", "POST"])
def sell_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        customer_name = request.form.get("customer_name")
        customer_phone = request.form.get("customer_phone")
        quantity = int(request.form.get("quantity"))
        sale_date = request.form.get("sale_date")

        if quantity <= 0:
            flash("Quantity must be greater than 0.", "error")
            return redirect(url_for("sell_product", product_id=product.id))

        if quantity > product.stock:
            flash("Not enough stock available!", "error")
            return redirect(url_for("sell_product", product_id=product.id))

        total_amount = product.sell_price * quantity
        profit = product.profit_per_unit() * quantity

        new_sale = Sale(
            customer_name=customer_name,
            customer_phone=customer_phone,
            quantity=quantity,
            total_amount=total_amount,
            profit=profit,
            sale_date=sale_date,
            product_id=product.id,
        )

        # Reduce stock after sale
        product.stock = product.stock - quantity

        db.session.add(new_sale)
        db.session.commit()

        flash("Sale completed successfully!", "success")
        return redirect(url_for("sales"))

    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("sell.html", product=product, today=today)


@app.route("/restock/<int:product_id>", methods=["GET", "POST"])
def restock_product(product_id):
    product = Product.query.get_or_404(product_id)

    if request.method == "POST":
        add_stock = int(request.form.get("add_stock"))
        buy_price = float(request.form.get("buy_price"))
        sell_price = float(request.form.get("sell_price"))

        if add_stock <= 0:
            flash("Stock quantity must be greater than 0.", "error")
            return redirect(url_for("restock_product", product_id=product.id))

        product.stock = product.stock + add_stock
        product.buy_price = buy_price
        product.sell_price = sell_price

        db.session.commit()

        flash("Product stock updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("restock.html", product=product)


@app.route("/sales")
def sales():
    all_sales = Sale.query.order_by(Sale.created_at.desc()).all()
    stats = get_dashboard_stats()
    return render_template("sales.html", sales=all_sales, stats=stats)


@app.route("/delete-sale/<int:sale_id>", methods=["POST"])
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)

    # Restore stock when sale is deleted
    sale.product.stock = sale.product.stock + sale.quantity

    db.session.delete(sale)
    db.session.commit()

    flash("Sale deleted and stock restored successfully!", "success")
    return redirect(url_for("sales"))


@app.route("/delete-product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    # Delete sales first, then delete product
    for sale in product.sales:
        db.session.delete(sale)

    db.session.delete(product)
    db.session.commit()

    flash("Product removed successfully!", "success")
    return redirect(url_for("home"))


@app.route("/about")
def about():
    return render_template("about.html")


# ----------------------------------------------------
# 6. Run the app
# ----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
