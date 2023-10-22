class Node:
    def __init__(self,key,value) -> None:
        self.value = value
        self.key = key
        self.next = None

class LinkedList:
    def __init__(self) -> None:
        self.head = None
    
    def append(self,key,value):
        if not self.head:
            self.head = Node(key,value)
            return
        current = self.head
        while current.next:
            if current.key == key:
                current.value = value
                return
            current = current.next
        current.next = Node(key,value)
    
    def remove(self,key):
        current = self.head
        if not current:
            return
        if current.key == key:
            self.head = current.next
            return
        while current.next:
            if current.next.key == key:
                current.next = current.next.next
                return
            current = current.next

    def find(self,key):
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None


class HashTable:
    def __init__(self,size) -> None:
        self.size = size
        self.count = 0 # This is the number of items in the table
        self.table = [LinkedList() for _ in range(self.size)]
    
    def _hash(self,key):
        return hash(key) % self.size
    
    def _resize(self):
        old_table = self.table
        self.size *= 2  # Double the size
        self.table = [LinkedList() for _ in range(self.size)]
        
        for ll in old_table:
            current = ll.head  # Access the head of the linked list
            while current:
                self.set(current.key, current.value, rehashing=True)
                current = current.next

    def set(self,key,value,rehashing=False):
        if not rehashing and self.count / self.size > 0.7:
            self._resize()
        
        index = self._hash(key)
        if not self.table[index].find(key):
            self.count += 1
        self.table[index].append(key,value)

    def get(self,key):
        index = self._hash(key)
        return self.table[index].find(key)
    
    def remove(self,key):
        index = self._hash(key)
        if self.table[index].find(key):
            self.count -= 1
        self.table[index].remove(key)

    def load_factor(self):
        return self.count / self.size
    
    def lookup(self,package_id):
        package = self.get(package_id)
        if package:
            return str(package)
        else:
            return "Package not found"

