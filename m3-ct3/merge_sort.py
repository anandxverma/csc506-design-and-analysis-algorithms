# Merge Sort - O(n log n) time complexity, O(n) space complexity
# Divide-and-conquer: recursively splits the array in half, sorts each half,
# then merges the two sorted halves back into one sorted array.

def merge_sort(arr):
    # Base case: arrays of length 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr

    # Split the array into two halves at the midpoint
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    # Merge two sorted arrays into one sorted array
    result = []
    i = j = 0

    # Compare elements from both halves and append the smaller one
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements from either half
    result.extend(left[i:])
    result.extend(right[j:])
    return result


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
        result = merge_sort(data.copy())
        print(f"Input:  {data}")
        print(f"Sorted: {result}")
        print()
