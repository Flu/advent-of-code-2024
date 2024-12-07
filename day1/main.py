def get_list_from_file(filename):
    list1 = []
    list2 = []
    with open(filename, "r") as f:
        while line := f.readline():
            numbers = line.split('   ')
            list1.append(numbers[0])
            list2.append(numbers[1])
    return list1, list2

list1, list2 = get_list_from_file("input.txt")
print(list1, list2)


list1.sort()
list2.sort()

result = 