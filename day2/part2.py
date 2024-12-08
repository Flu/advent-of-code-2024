# Advent of Code 2024 - Day 2, Part 2
# Task Description:
# Given a list of reports, find out if a report is safe. A report is safe in one of the following ways:
# If the numbers in the report are always increasing or always decreasing (equal is not allowed), then they're safe
# if the delta between them is no larger than 3.
# In other words, for any a(i) in that report, 0 < abs(a(i)- a(i-1)) <= 3. 
# 
# Link: https://adventofcode.com/2024/day/2
# Author: Adrian Fluturel
# Email: fluturel.adrian@gmail.com
# Date: 2024-12-04
#
# License: MIT License

def read_reports_from_file(filename):
    """Parse inputs from the input file"""
    reports = []
    with open(filename, "r") as f:
        while line := f.readline():
            numbers = line.split(" ")
            report = [int(x) for x in numbers]
            reports.append(report)
    return reports

def check_stability(report):
    """Checks if a report is stable and returns True if it, False otherwise"""
    increasing = True
    decreasing = True
    max_change = 0
    for i in range(len(report)-1):
        max_change = max(max_change, abs(report[i] - report[i+1]))
        # If delta between two levels is greater than 3, it is not safe
        if max_change > 3:
            return False
        # If delta is 0 or not monotonically increasing or decreasing, it is not safe
        if report[i] <= report[i+1]:
            decreasing = False
        if report[i] >= report[i+1]:
            increasing = False
    # Print if report increasing, decreasing and the maximum delta change in levels
    print(report, increasing, decreasing, max_change)
    # Check for stability
    if increasing is False and decreasing is False:
        return False
    return True
    

reports = read_reports_from_file("reports.txt")

number_of_stable = 0

# Check each report for stability
for report in reports:
    at_least_one_safe = False
    # Because of stability dampeners, we can safely ignore a bigger delta then allowed
    # and still classify the report as safe
    for i in range(len(report)):
        mutated_report = report[:]
        del mutated_report[i]
        if check_stability(mutated_report):
            at_least_one_safe = True
            break
    # Keep track of how many reports are deemed safe after correction
    if at_least_one_safe:
        number_of_stable += 1

# Print result
print(number_of_stable)