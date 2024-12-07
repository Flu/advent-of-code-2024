file_string = ""
with open("input.txt", "r") as f:
    file_string = f.readlines()

# Join all the lines into one big string since we don't care about different lines
file_string = "".join(file_string)

# Use regex to extract the numbers with capture groups
# This is much less work than it would have been just parsing it normally
import re
p = re.compile(r"mul\(([\d]+),([\d]+)\)")
results = p.findall(file_string)

# For all matches, we can extract the numbers from their respective capture groups, parse them as ints
# and multiply them and finally add them to the final sum 
final_sum = 0
enable_mul = True
for result in results:
    number1 = int(result[0])
    number2 = int(result[1])
    final_sum += number1 * number2

print(final_sum)
