class MyDictionary:
    def __init__(self):
        self.keys = []
        self.values = []

    def __getitem__(self, key):
        if key in self.keys:
            index = self.keys.index(key)
            return self.values[index]
        else:
            raise KeyError(f"Key '{key}' not found")

    def __setitem__(self, key, value):
        if key in self.keys:
            index = self.keys.index(key)
            self.values[index] = value
        else:
            self.keys.append(key)
            self.values.append(value)

    def __contains__(self, key):
        return key in self.keys

    def keys(self):
        return self.keys

    def values(self):
        return self.values

    def items(self):
        return zip(self.keys, self.values)


# örnek kullanım
my_dict = MyDictionary()
my_dict['username1'] = 'Alice'
my_dict['username2'] = 'Bob'

print(my_dict['username1'])  # Output: Alice

print('username2' in my_dict)  # Output: True

for key, value in my_dict.items():
    print(f"Key: {key}, Value: {value}")
