# function to calculate average of a list of numbers 
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    total = sum(numbers)
    average = total / len(numbers)
    return average
# test the function with a sample list of numbers
sample_numbers = [10, 20, 30, 40, 50]
average_result = calculate_average(sample_numbers)
print(f"The average of the sample numbers is: {average_result}")
