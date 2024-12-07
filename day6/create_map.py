result = ""
width = 500
height = 500

import random as r

for i in range(height):
    row = r.choices([".", "#"], [0.99, 0.01], k=width)
    result += "".join(row) + "\n"

with open("ultra_test.txt", "w") as f:
    f.write(result)