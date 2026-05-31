# Insertion Sort - O(n^2) time complexity, O(1) space complexity
# Builds the sorted region one element at a time by taking each new element
# and shifting it left until it sits in its correct sorted position.
def insertion_sort(arr):
    n = len(arr)
    # arr[0..i-1] is always sorted; start from index 1 since a single element is trivially sorted
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        # Shift elements of arr[0..i-1] that are greater than key one position to the right
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        # Insert key into its correct position in the sorted region
        arr[j + 1] = key
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
        result = insertion_sort(data.copy())
        print(f"Input:  {data}")
        print(f"Sorted: {result}")
        print()
