combined_weight = 0 
total_weight = 0
packages_sent = 0
items_amount_current = 0
not_optimal = 0
not_optimal_weight = 0
max_not_optimal_weight = 0
item_weight = ""

# 1. Ask user for the number of items
amount = int(input("Please enter amount of items to be shiped: "))

#  --- loop ---
for items_amount in range(1, amount +1):
    while True:
        item_weight_input= (input(f"Please enter weight of individual item {items_amount}(0 to end): ")) #user input with msg
        if item_weight_input.strip() == "": # verifie input was entered and it is not space
            print("No input provided. Please enter the weight of the item.")
            continue
        try: # verification of input, must be number and between 1-10, breaking loop if 0 is entered
            item_weight = int(item_weight_input)
            if item_weight == 0:
                print("Zero entered, ending the program")
                break
            elif item_weight < 0 or item_weight > 10:
                print("Invalid weight! Weight should be between 1 and 10 kg.")
                continue
        except ValueError:
            print("Invalid input! Please enter a valid number for item weight.")
            continue
        
       
        if item_weight + combined_weight > 20:  # calculations
            packages_sent += 1
            total_weight += combined_weight
            not_optimal_weight += 20 - combined_weight
            if 20 - combined_weight > max_not_optimal_weight:
                max_not_optimal_weight = 20 - combined_weight
                not_optimal = packages_sent
            print(f"Package {packages_sent } with {items_amount_current} items of total weight of {combined_weight}kg" )
            combined_weight = 0
            items_amount_current = 0

        

        combined_weight += item_weight
        items_amount_current +=1
        break
    
    if item_weight == 0: # terminating program if 0 was entered
        break

if items_amount_current > 0: # calculations
    print(f"Package {packages_sent + 1} with {items_amount_current} items of total weight of {combined_weight}kg" )
    packages_sent += 1
    total_weight += combined_weight
    not_optimal_weight += 20 - combined_weight
    if 20 - combined_weight > max_not_optimal_weight:
            max_not_optimal_weight = 20 - combined_weight
            not_optimal = packages_sent

unused_capacity = (packages_sent * 20) - total_weight


# output massage
print("\nNumber of packages sent: ", packages_sent)           
print("Total weight in packages sent: ",total_weight )
print(f"Total 'unused' capacity (non-optimal packaging): {unused_capacity}kg")
print(f"The package number {not_optimal} had the most 'unused' capacity and the amount of 'unused' capacity in that package was {max_not_optimal_weight}kg")
