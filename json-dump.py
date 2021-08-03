import pickle
obj1 = {'name': 'Nora', 'age': 0}
obj2 = ('t', 'u', 'p', 'l', 'e')
fileName = 'dumped.txt'
with open(fileName, 'wb+') as f:
    pickle.dump(obj1, f) #serialize obj1
    pickle.dump(obj2, f) #serialize obj2

with open(fileName, 'rb') as f:
    obj1Reloaded = pickle.load(f) #deserialize obj1
    obj2Reloaded = pickle.load(f) #deserialize obj2