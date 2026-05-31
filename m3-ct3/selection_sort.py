# Selection Sort - O(n^2) time complexity, O(1) space complexity
# Repeatedly finds the minimum element in the unsorted portion and
# swaps it into the next sorted position, growing the sorted region left to right.
def selection_sort(arr):
    n = len(arr)
    # After each pass, position i holds its final sorted value,
    # so we only need to scan from i+1 onward for the next minimum.
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        # Swap the minimum found into the current sorted boundary
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

if __name__ == "__main__":
    # Test cases: general, small, single element, empty, duplicates
    samples = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 1, 4, 2, 8],
        [1],
        [],
        [3, 3, 3, 1, 2],
    ]

    for data in samples:
        result = selection_sort(data.copy())
        print(f"Input:  {data}")
        print(f"Sorted: {result}")
        print()
