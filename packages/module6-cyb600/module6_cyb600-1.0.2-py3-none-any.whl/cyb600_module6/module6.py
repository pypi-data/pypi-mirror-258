def only_odd_numbers(arr):
    pass

def only_even_numbers(arr):
    if not isinstance(arr, list):
        return []
    # iterating each number in list
    output_arr = []
    for num in arr:
        # checking condition
        if num % 2 != 0:
            output_arr.append(num)
    return output_arr
