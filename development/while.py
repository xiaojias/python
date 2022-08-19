# Get the result of Factorial for a input number (1 * 2 * ... * n)
print("Enter number:")
number = int(input())

number_entered = number

fac = 1

if number == 0:
    result = 1
else:
    while number >= 1:
        fac = fac * number
        number -= 1
    result = fac

print("Factorial of {} is {}.".format(number_entered, result))



