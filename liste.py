class MyList:
    def __init__(self):
        self.elements = []
        self.index = 0

    def append(self, element):
        self.elements += [element]

    def get(self, index):
        if 0 <= index < len(self.elements):
            return self.elements[index]
        else:
            raise IndexError("Index out of range")

    def remove(self, element):
        if element in self.elements:
            self.elements = [e for e in self.elements if e != element]
        else:
            raise ValueError("Element not found")

    def size(self):
        return len(self.elements)

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < len(self.elements):
            result = self.elements[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
