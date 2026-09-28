class Jar:
    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError
        self._size = 0
        self._capacity = capacity

    def __str__(self):
        return "🍪" * self._size

    def deposit(self, n):
        if self._capacity < (n + self._size):
            raise ValueError
        self._size += n

    def withdraw(self, n):
        if self._size < n:
            raise ValueError
        self._size -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, n):
        self._size = n
