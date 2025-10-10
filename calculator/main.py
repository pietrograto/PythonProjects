import os
from art import logo

def add(n1, n2):
  """Add two numbers."""
  return n1 + n2

def subtract(n1, n2):
  """Subtract second number from first."""
  return n1 - n2

def multiply(n1, n2):
  """Multiply two numbers."""
  return n1 * n2

def divide(n1, n2):
  """Divide first number by second."""
  return n1 / n2

operations = {
  "+": add,
  "-": subtract,
  "*": multiply,
  "/": divide
}

def calculator():
  """Main calculator function with continuous operation support."""
  print(logo)

  num1 = float(input("What's the first number?: "))
  for symbol in operations:
    print(symbol)
  should_continue = True
 
  while should_continue:
    operation_symbol = input("Pick an operation: ")
    if operation_symbol not in operations:
        print("the provided operation is not an operation. ")
        operation_symbol=input("Pick a new operation: ")

    num2 = float(input("What's the next number?: "))
    calculation_function = operations[operation_symbol]
    answer = calculation_function(num1, num2)
    print(f"{num1} {operation_symbol} {num2} = {answer}")

    if input(f"Type 'y' to continue calculating with {answer}, or type 'n' to start a new calculation: ") == 'y':
      num1 = answer
    else:
      should_continue = False
      os.system("clear")
      calculator()

calculator()
