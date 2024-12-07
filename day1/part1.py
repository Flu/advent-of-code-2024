def get_lists_from_file(filename):
    list1 = []
    list2 = []
    with open(filename, "r") as f:
        while line := f.readline():
            numbers = line.split('   ')
            list1.append(int(numbers[0]))
            list2.append(int(numbers[1]))
    return list1, list2

# Extract lists from the input file
list1, list2 = get_lists_from_file("input.txt")

# Sort all the lists so we can compare the smallest elements
list1.sort()
list2.sort()

# Get the absolute value of the difference of all elements in the sorted list
result = sum([abs(list1[i]-list2[i]) for i in range(len(list1))])
print("The difference between the lists:", result)