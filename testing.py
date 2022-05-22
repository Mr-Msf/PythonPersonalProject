n_of_sides = int(input("How many sides does your shape have: "))
total_angles = (n_of_sides - 2) * 180
running_total = 0

for num in range(n_of_sides - 1):
    running_total = running_total + int(input("Angle " + str(num + 1) + ": "))

angle_final = total_angles - running_total

print("The final angle in your shape is " + str(angle_final) + " degrees.")