n_of_sides = int(input("How many sides does your shape have?\n"))
running_total = 0

for i in range(n_of_sides):
    print(i)
    running_total = running_total + int(input("Angle: "))

while True:
    n_of_sides = 2

    if n_of_sides == 0:
        break

angle1 = int(input("\nAngle 1: "))
angle2 = int(input("\nAngle 2: "))



angle_final = running_total

print("\nAngle 3: " + str(angle_final) + "\n")