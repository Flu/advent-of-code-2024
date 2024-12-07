def read_reports_from_file(filename):
    reports = []
    with open(filename, "r") as f:
        while line := f.readline():
            numbers = line.split(" ")
            report = [int(x) for x in numbers]
            reports.append(report)
    return reports

def check_stability(report):
    increasing = True
    decreasing = True
    max_change = 0
    for i in range(len(report)-1):
        max_change = max(max_change, abs(report[i] - report[i+1]))
        if max_change > 3:
            return False
        if report[i] <= report[i+1]:
            decreasing = False
        if report[i] >= report[i+1]:
            increasing = False
    print(report, increasing, decreasing, max_change)
    if increasing is False and decreasing is False:
        return False
    return True
    

reports = read_reports_from_file("test.txt")

number_of_stable = 0
for report in reports:
    number_of_stable += 1 if check_stability(report) else 0

print(number_of_stable)