from pybloomfilter import BloomFilter
fruit = BloomFilter(100000, 0.1, 'words.bloom')
fruit.update(('apple', 'pear', 'orange', 'apple'))
# print(len(fruit))
if 'apple' in fruit:
    print('True')
fruit.update(['1','2','3','4'])
print(len(fruit))
fruit=fruit.clear_all()
print(fruit)
fruit = BloomFilter(100000, 0.1, 'words.bloom')
fruit.update(['1','2','3','4'])
print(len(fruit))