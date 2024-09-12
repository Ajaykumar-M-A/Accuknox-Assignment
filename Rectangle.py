class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        return iter([{'length': self.length}, {'width': self.width}])


# Example usage:
rect = Rectangle(7, 14)

# Iterating over the instance
for dimension in rect:
    print(dimension)
