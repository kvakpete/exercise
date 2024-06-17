from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class Operation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    
    def __repr__(self):
        return f'<Operation {self.id}: {self.description} at {self.timestamp}>'

class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

# Utility function to get or create balance
def get_balance():
    balance = Balance.query.first()
    if not balance:
        balance = Balance(amount=0.0)
        db.session.add(balance)
        db.session.commit()
    return balance

@app.route('/')
def index():
    balance = get_balance().amount
    products = Product.query.all()
    warehouse = {product.name: {'price': product.price, 'quantity': product.quantity} for product in products}
    return render_template('index.html', balance=balance, warehouse=warehouse)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        name = request.form['product_name']
        price = float(request.form['unit_price'])
        quantity = int(request.form['number_of_pieces'])
        balance = get_balance()

        purchase_amount = price * quantity
        if balance.amount >= purchase_amount:
            balance.amount -= purchase_amount
            product = Product.query.filter_by(name=name).first()
            if product:
                product.quantity += quantity
            else:
                product = Product(name=name, price=price, quantity=quantity)
                db.session.add(product)
            operation = Operation(description=f"Purchased {quantity} of {name} for €{purchase_amount}")
            db.session.add(operation)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash("Insufficient balance.")
    
    balance = get_balance().amount
    products = Product.query.all()
    warehouse = {product.name: {'price': product.price, 'quantity': product.quantity} for product in products}
    return render_template('purchase.html', balance=balance, warehouse=warehouse)

@app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        name = request.form['product_name']
        price = float(request.form['unit_price'])
        quantity = int(request.form['number_of_pieces'])
        balance = get_balance()

        product = Product.query.filter_by(name=name).first()
        if product and product.quantity >= quantity:
            product.quantity -= quantity
            sale_amount = price * quantity
            balance.amount += sale_amount
            operation = Operation(description=f"Sold {quantity} of {name} for €{sale_amount}")
            db.session.add(operation)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            flash("Insufficient stock or product not found.")
    
    balance = get_balance().amount
    products = Product.query.all()
    warehouse = {product.name: {'price': product.price, 'quantity': product.quantity} for product in products}
    return render_template('sale.html', balance=balance, warehouse=warehouse)

@app.route('/balance', methods=['GET', 'POST'])
def change_balance():
    if request.method == 'POST':
        operation_type = request.form['operation_type']
        value = float(request.form['value'])
        balance = get_balance()

        if operation_type == 'add':
            balance.amount += value
            operation = Operation(description=f"Added €{value} to balance")
        elif operation_type == 'subtract':
            if balance.amount >= value:
                balance.amount -= value
                operation = Operation(description=f"Subtracted €{value} from balance")
            else:
                flash("Insufficient balance.")
                return redirect(url_for('change_balance'))
        
        db.session.add(operation)
        db.session.commit()
        return redirect(url_for('index'))
    
    balance = get_balance().amount
    products = Product.query.all()
    warehouse = {product.name: {'price': product.price, 'quantity': product.quantity} for product in products}
    return render_template('balance.html', balance=balance, warehouse=warehouse)

@app.route('/history')
def history():
    from_index = request.args.get('line_from', default=0, type=int)
    to_index = request.args.get('line_to', default=None, type=int)

    operations = Operation.query.slice(from_index, to_index).all()
    total_operations = Operation.query.count()
    
    balance = get_balance().amount
    products = Product.query.all()
    warehouse = {product.name: {'price': product.price, 'quantity': product.quantity} for product in products}
    return render_template('history.html', operations=operations, balance=balance, warehouse=warehouse, operations_len=total_operations, from_index=from_index, to_index=to_index)

if __name__ == '__main__':
    app.run(debug=True)
