# Check the length of Collatz sequence for the given x
count = 0
try:
    x = int(input("Enter a number (1-100): "))
    if x < 1 or x > 100:
        print("Error: x must be in the range 1-100.")
        exit(1)
    while x != 1:
        if x % 2 == 0:
            x //= 2
        else:
            x = 3 * x + 1
        count += 1
    print("Length of Collatz sequence:", count)
except ValueError:
    print("Error: Invalid input. Please enter an integer.")
    exit(1)
