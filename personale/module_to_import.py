# module_to_import.py

def greet(x, y, z):
    print("Hello,", x, y + ",", "the", z + "!")

# x = "Angela"
# y = "Davis"
# z = "scholar"

name = "Angela"
second_name = "Davis"
profession = "scholar"

# questa parte verrà stampata solo se viene eseguita come script a se stante
# se viene importata, non verrà stampata perchè non sarebbe più main
if __name__ == "__main__":
    print("module 2: ", __name__)
    print("Ciao a tutti")

