import pickle

test_results = {}

with open('test_results', 'rb') as f:
    test_results = pickle.load(f)

print(test_results)
