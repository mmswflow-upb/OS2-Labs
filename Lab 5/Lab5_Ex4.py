import sys

def compute(a,b,c,d):
    if a < 10 and b < 10 and c < 10 and d < 10:
        return str(a + b * c + d)
    else:
        return "Invalid Input, Numbers must be less than 10"
    

try:
    a = float(input("Input a:"))
    b = float(input("Input b:"))
    c = float(input("Input c:"))
    d = float(input("Input d:"))
    print("The result is: " + compute(a,b,c,d))

except:
    print("Invalid input, please enter a number.")
    sys.exit(0)