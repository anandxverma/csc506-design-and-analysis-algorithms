# Bubble Sort - O(n^2) time complexity, O(1) space complexity
# Repeatedly swaps adjacent elements that are out of order,
# "bubbling" the largest unsorted element to its correct position each pass.
def bubble_sort(arr):
    n = len(arr)
    # Each pass guarantees the largest element in the unsorted region
    # moves to its final position, so we shrink the range by i each time.
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
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
        result = bubble_sort(data.copy())
        print(f"Input:  {data}")
        print(f"Sorted: {result}")
        print()
