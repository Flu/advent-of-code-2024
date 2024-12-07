file_string = ""
with open("input.txt", "r") as f:
    file_string = f.readlines()

file_string = "".join(file_string)

import re
p = re.compile("mul\(([\d]+),([\d]+)\)|(do\(\))|(don't\(\))")
results = p.findall(file_string)

print(results)
final_sum = 0
enable_mul = True
for result in results:
    if result[2] == "do()":
        enable_mul = True
    elif result[3] == "don't()":
        enable_mul = False
    elif enable_mul == True:
        number1 = int(result[0])
        number2 = int(result[1])
        final_sum += number1 * number2

print(final_sum)
