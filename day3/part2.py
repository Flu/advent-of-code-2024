file_string = ""
with open("input.txt", "r") as f:
    file_string = f.readlines()

# Join all the lines into one big string since we don't care about different lines
file_string = "".join(file_string)

# Use regex to extract the numbers with capture groups
# This is much less work than it would have been just parsing it normally
# Note: Now we will have two more capture groups that we can use to identify in which case we are
import re
p = re.compile(r"mul\(([\d]+),([\d]+)\)|(do\(\))|(don't\(\))")
results = p.findall(file_string)


final_sum = 0

# By default, multiplication is enabled
enable_mul = True

# For all matches, we can extract the numbers from their respective capture groups, parse them as ints
# and multiply them and finally add them to the final sum, if multiplication is enabled
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
