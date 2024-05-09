def binary_search(arr, x):
    low = 0
    high = len(arr) - 1
    iterations = 0
 
    while low <= high:
 
        mid = (high + low) // 2
        iterations += 1

        # якщо x більше за значення посередині списку, ігноруємо ліву половину
        if arr[mid] < x:
            low = mid + 1
 
        # якщо x менше за значення посередині списку, ігноруємо праву половину
        elif arr[mid] > x:
            high = mid - 1
        else:
            return iterations, arr[mid]
 
    upper_bound = None
    if low < len(arr):
        upper_bound = arr[low]

    return iterations, upper_bound

arr = [0.5, 1.5, 2.5, 2.75, 4.5, 5.15, 5.25, 6.2]
x = 6.2
iterations, upper_bound = binary_search(arr, x)
print(f"Iteration count: {iterations}")
print(f"Upper bound: {upper_bound}")
