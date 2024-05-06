def add_balance(balance, amount):
    return balance + amount

def subtract_balance(balance, amount):
    if balance >= amount:
        return balance - amount, True
    else:
        print("Insufficient balance.")
        return balance, False

def add_product(warehouse, name, price, quantity):
    if name in warehouse:
        warehouse[name]['quantity'] += quantity
    else:
        warehouse[name] = {'price': price, 'quantity': quantity}

def remove_product(warehouse, name, quantity):
    if name in warehouse:
        if warehouse[name]['quantity'] >= quantity:
            warehouse[name]['quantity'] -= quantity
            return True
        else:
            print("Insufficient quantity in warehouse.")
            return False
    else:
        print("Product not found in warehouse.")
        return False

def get_product_status(warehouse, name):
    if name in warehouse:
        return warehouse[name]
    else:
        return None

def list_inventory(warehouse):
    print("Warehouse Inventory:")
    for product, details in warehouse.items():
        print(f"Product: {product}, Price: {details['price']}, Quantity: {details['quantity']}")

def review_operations(operations, from_index=None, to_index=None):
    if from_index is None and to_index is None:
        print("Recent Operations:")
        for op in operations:
            print(op)
        return

    if from_index is None:
        from_index = 0
    if to_index is None:
        to_index = len(operations) - 1

    if from_index < 0 or to_index >= len(operations) or from_index > to_index:
        print("Invalid index range.")
        return

    print("Recent Operations:")
    for i in range(from_index, to_index + 1):
        print(operations[i])

def main():
    account_balance = 0
    warehouse = {}
    operations = []
    commands = {
        '1': 'balance',
        '2': 'sale',
        '3': 'purchase',
        '4': 'account',
        '5': 'list',
        '6': 'warehouse',
        '7': 'review',
        '8': 'end'
    }

    while True:
        print("\nAvailable Commands:")
        print("1 - balance - Add/subtract from account balance")
        print("2 - sale - Record a sale")
        print("3 - purchase - Record a purchase")
        print("4 - account - Display account balance")
        print("5 - list - List warehouse inventory")
        print("6 - warehouse - Check product status in warehouse")
        print("7 - review - Review recorded operations")
        print("8 - end - Terminate the program")

        command_input = input("Enter command by number or name: ").strip().lower()

        if command_input in commands:
            command = commands[command_input]
        else:
            command = command_input

        if command == 'balance':
            amount = float(input("Enter amount to add/subtract: "))
            account_balance = add_balance(account_balance, amount)
            operations.append(f"Added {amount} to account balance")
        elif command == 'sale':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter quantity sold: "))
            sale_amount = price * quantity
            if remove_product(warehouse, name, quantity):
                account_balance = add_balance(account_balance, sale_amount)
                operations.append(f"Sold {quantity} of {name} for ${sale_amount}")
        elif command == 'purchase':
            name = input("Enter product name: ")
            price = float(input("Enter product price: "))
            quantity = int(input("Enter quantity purchased: "))
            purchase_amount = price * quantity
            account_balance, success = subtract_balance(account_balance, purchase_amount)
            if success:
                add_product(warehouse, name, price, quantity)
                operations.append(f"Purchased {quantity} of {name} for ${purchase_amount}")
        elif command == 'account':
            print("Account Balance:", account_balance)
        elif command == 'list':
            list_inventory(warehouse)
        elif command == 'warehouse':
            name = input("Enter product name: ")
            status = get_product_status(warehouse, name)
            if status:
                print("Product:", name)
                print("Price:", status['price'])
                print("Quantity:", status['quantity'])
            else:
                print("Product not found in warehouse.")
        elif command == 'review':
            from_index = input("Enter 'from' index (leave empty for beginning): ")
            to_index = input("Enter 'to' index (leave empty for end): ")
            if from_index.strip() == '':
                from_index = None
            if to_index.strip() == '':
                to_index = None
            if (from_index is None or from_index.isdigit()) and (to_index is None or to_index.isdigit()):
                review_operations(operations, int(from_index) if from_index is not None else None, int(to_index) if to_index is not None else None)
            else:
                print("Invalid index input.")
        elif command == 'end':
            print("Exiting the program...")
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
