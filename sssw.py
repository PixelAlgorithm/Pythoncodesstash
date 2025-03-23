def calculator():
    print("Simple Calculator")
    print("----------------")
    print("Operations:")
    print("1. Addition (+)")
    print("2. Subtraction (-)")
    print("3. Multiplication (*)")
    print("4. Division (/)")
    
    while True:
        try:
            # Get user input
            choice = input("\nSelect operation (1-4): ")
            if choice not in ['1', '2', '3', '4']:
                print("Invalid choice! Please select 1-4")
                continue
                
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            # Perform calculation based on choice
            if choice == '1':
                result = num1 + num2
                print(f"\n{num1} + {num2} = {result}")
                
            elif choice == '2':
                result = num1 - num2
                print(f"\n{num1} - {num2} = {result}")
                
            elif choice == '3':
                result = num1 * num2
                print(f"\n{num1} * {num2} = {result}")
                
            elif choice == '4':
                if num2 == 0:
                    print("\nError: Cannot divide by zero!")
                else:
                    result = num1 / num2
                    print(f"\n{num1} / {num2} = {result}")
            
            # Ask if user wants to continue
            again = input("\nDo you want to perform another calculation? (yes/no): ")
            if again.lower() != 'yes':
                print("\nThank you for using the calculator!")
                break
                
        except ValueError:
            print("Invalid input! Please enter valid numbers.")
            
if __name__ == "__main__":
    calculator()
