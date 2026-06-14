# Hash Table implementation using chaining for collision resolution.
# Each bucket is a list of (key, value) tuples; multiple keys can map
# to the same bucket index without overwriting each other.
class HashTable:
    def __init__(self, size=10):
        """Initialize the table with `size` empty buckets."""
        self.size = size
        # Initialize each bucket as an empty list to hold chained pairs
        self.buckets = [[] for _ in range(self.size)]

    def _hash(self, key):
        """Return the bucket index for `key` by summing its character ASCII values mod table size."""
        # Sum ASCII values of the key's characters, then wrap to table size
        return sum(ord(c) for c in str(key)) % self.size

    def insert(self, key, value):
        """Insert `key`/`value` into the table, or update the value if `key` already exists."""
        index = self._hash(key)
        bucket = self.buckets[index]
        # Update value in-place if key already exists (avoid duplicates)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        """Return the value associated with `key`, or raise KeyError if not found."""
        index = self._hash(key)
        for k, v in self.buckets[index]:
            if k == key:
                return v
        raise KeyError(f"Key '{key}' not found")

    def delete(self, key):
        """Remove the entry for `key` from the table, or raise KeyError if not found."""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                return
        raise KeyError(f"Key '{key}' not found")

    def display_buckets(self):
        """Print each non-empty bucket index alongside its full chain of (key, value) pairs."""
        for i, bucket in enumerate(self.buckets):
            if bucket:
                chain = " -> ".join(f"({k!r}: {v!r})" for k, v in bucket)
                print(f"  [{i}]: {chain}")

    def __str__(self):
        """Return a dict-like string of all key/value pairs across every bucket."""
        # Flatten all buckets into a single list of pairs for display
        pairs = []
        for bucket in self.buckets:
            pairs.extend(bucket)
        return "{" + ", ".join(f"{k!r}: {v!r}" for k, v in pairs) + "}"


if __name__ == "__main__":
    ht = HashTable()

    # "age", "city", and "run" all hash to index 1 (ASCII sums 301, 441, 341 — all % 10 == 1)
    # — deliberate collisions to show chaining in action
    ht.insert("name", "Alice")   # index 7
    ht.insert("age", 30)         # index 1
    ht.insert("city", "Denver")  # index 1  <-- collides with "age"
    ht.insert("run", 5)          # index 1  <-- also collides

    print("Bucket layout after inserting colliding keys:")
    ht.display_buckets()
    # Expected: bucket [1] holds a chain of three pairs

    print("\nget('age')  ->", ht.get("age"))
    print("get('city') ->", ht.get("city"))
    print("get('run')  ->", ht.get("run"))

    # In-place update: replaces only the matching pair in the chain
    ht.insert("age", 31)
    print("\nAfter updating age:")
    ht.display_buckets()

    # Delete one entry from the colliding bucket; remaining chain is intact
    ht.delete("city")
    print("\nAfter deleting city:")
    ht.display_buckets()
