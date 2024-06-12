from flask import Flask, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Load initial data
balance, warehouse, operations = 0, {}, []
try:
    with open("company_data.json", "r") as file:
        data = json.load(file)
        balance = data.get("balance", 0)
        warehouse = data.get("warehouse", {})
        operations = data.get("operations", [])
except FileNotFoundError:
    print("No previous data found. Starting with default values.")

def save_data():
    try:
        with open("company_data.json", "w") as file:
            data = {
                "balance": balance,
                "warehouse": warehouse,
                "operations": operations
            }
            json.dump(data, file)
        print("Data saved successfully.")
    except Exception as e:
        print(f"Error occurred while saving data: {e}")

@app.route('/')
def index():
    return render_template('index.html', balance=balance, warehouse=warehouse)

@app.route('/purchase', methods=['GET', 'POST'] )
def purchase():
    if request.method == 'POST':
        name = request.form['product_name']
        price = float(request.form['unit_price'])
        quantity = int(request.form['number_of_pieces'])
        global balance, operations

        purchase_amount = price * quantity
        if balance >= purchase_amount:
            balance -= purchase_amount
            if name in warehouse:
                warehouse[name]['quantity'] += quantity
            else:
                warehouse[name] = {'price': price, 'quantity': quantity}
            operations.append(f"Purchased {quantity} of {name} for €{purchase_amount}")
            save_data()
            return redirect(url_for('index'))
        else:
            flash("Insufficient balance.")
    
    return render_template('purchase.html', balance=balance, warehouse=warehouse)

@app.route('/sale', methods=['GET', 'POST'])
def sale():
    if request.method == 'POST':
        name = request.form['product_name']
        price = float(request.form['unit_price'])
        quantity = int(request.form['number_of_pieces'])
        global balance, operations

        if name in warehouse and warehouse[name]['quantity'] >= quantity:
            warehouse[name]['quantity'] -= quantity
            sale_amount = price * quantity
            balance += sale_amount
            operations.append(f"Sold {quantity} of {name} for ${sale_amount}")
            save_data()
            return redirect(url_for('index'))
        else:
            flash("Insufficient stock or product not found.")
    
    return render_template('sale.html', balance=balance, warehouse=warehouse)

@app.route('/balance', methods=['GET', 'POST'])
def change_balance():
    if request.method == 'POST':
        operation_type = request.form['operation_type']
        value = float(request.form['value'])
        global balance, operations

        if operation_type == 'add':
            balance += value
            operations.append(f"Added ${value} to balance")
        elif operation_type == 'subtract':
            if balance >= value:
                balance -= value
                operations.append(f"Subtracted €{value} from balance")
            else:
                flash("Insufficient balance.")
                return redirect(url_for('change_balance'))
        
        save_data()
        return redirect(url_for('index'))
    
    return render_template('balance.html', balance=balance, warehouse=warehouse)


@app.route('/history')
def history():
    from_index = request.args.get('line_from', default=0, type=int)
    to_index = request.args.get('line_to', default=len(operations), type=int)

    if from_index < 0 or to_index > len(operations) or from_index > to_index:
        flash("Invalid index range.")
        return redirect(url_for('index'))

    return render_template('history.html', operations=operations[from_index:to_index], balance=balance, warehouse=warehouse, operations_len=len(operations), from_index=from_index, to_index=to_index)

if __name__ == '__main__':
    app.run(debug=True)