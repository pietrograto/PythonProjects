from data import MENU, resources

profit = 0
is_on = True

def refill_resources(refill_item, refill_value):
    """Refill resources if necessary."""
    if refill_item in resources:
        resources[refill_item] += int(refill_value)
        print(f"Refilled {refill_item} by {refill_value}.")
    else:
        print(f"Invalid refill item: {refill_item}")

def is_resource_sufficient(order_ingredients):
    """Returns True when the order can be made, False if ingredients are insufficient."""
    global is_on
    
    for item in order_ingredients:
        if order_ingredients[item] > resources[item]:
            print(f"Sorry, there is not enough {item}.")
            refill = input("Would you like to refill? Type 'yes' if you want, otherwise type 'no' ").lower()
            if refill == "yes":
                refill_item = input("What would you like to refill? Type water, milk, or coffee: ").lower()
                if refill_item in resources:
                    refill_value = input(f"Type the ml/g of {refill_item}: ")
                    refill_resources(refill_item, refill_value)
                else:
                    print(f"Invalid refill item: {refill_item}")
                    return False
                # Print report before refill
                # print_report()
                # refill_resources(order_ingredients)
                # Print report after refill
                # print_report()
            else:
                is_on = False
                return False
    return True

def print_report():
    """Prints the current state of resources."""
    print(f"Water: {resources['water']}ml")
    print(f"Milk: {resources['milk']}ml")
    print(f"Coffee: {resources['coffee']}g")
    print(f"Money: ${profit}")

def process_coins():
    """Returns the total calculated from coins inserted."""
    print("Please insert coins.")
    total = int(input("How many quarters?: ")) * 0.25
    total += int(input("How many dimes?: ")) * 0.1
    total += int(input("How many nickels?: ")) * 0.05
    total += int(input("How many pennies?: ")) * 0.01
    return total

def is_transaction_successful(money_received, drink_cost):
    """Returns True when the payment is accepted, or False if money is insufficient."""
    global profit
    if money_received >= drink_cost:
        change = round(money_received - drink_cost, 2)
        print(f"Here is ${change} in change.")
        profit += drink_cost
        return True
    else:
        print("Sorry, that's not enough money. Money refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    """Deduct the required ingredients from the resources."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name} ☕️. Enjoy!")

def main():
    global is_on

    while is_on:
        coffee = input("What would you like? (espresso/latte/cappuccino/turn off/report): ").lower()

        if coffee == "off":
            is_on = False
        elif coffee == "report":
            print_report()
        else:
            if coffee in MENU:
                drink = MENU[coffee]
                if is_resource_sufficient(drink["ingredients"]):
                    payment = process_coins()
                    if is_transaction_successful(payment, drink["cost"]):
                        make_coffee(coffee, drink["ingredients"])
                        print("Enjoy your coffee!")
            else:
                print("Invalid choice. Please select a valid drink.")

if __name__ == "__main__":
    main()