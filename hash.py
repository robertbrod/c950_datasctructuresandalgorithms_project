class HashTable:
    def __init__(self, size=10):
        self.table = []
        for i in range(size):
            self.table.append([])

    def insert(self, object):
        bucket = hash(object.id) % len(self.table)
        self.table[bucket].append(object)

    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for object in bucket_list:
            if object.id == key: 
                index = bucket_list.index(object)

                return bucket_list[index]

        print("Key not found")
        return None

    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for object in bucket_list:
            if object.id == key:
                index = bucket_list.index(object)

                bucket_list.pop(index)