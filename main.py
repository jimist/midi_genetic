import mido
from mido import MidiFile

from os import listdir
from os.path import isfile, join

import pickle

import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier

from genetic import Genetic

TEST_FILES_DIRECTORY = "song_sources/test_set/"


def extract_data_from_file(file_path):
    mid = MidiFile(file_path)
    vectors = []

    for i, track in enumerate(mid.tracks):
        for msg in track:
            if hasattr(msg, 'note'):
                vectors.append(msg.note)

    data = []
    labels = []

    return vectors


# train_file_names = [f for f in listdir('dataset/train_set/') if isfile(join('dataset/train_set/', f))]
test_file_names = [f for f in listdir(TEST_FILES_DIRECTORY) if isfile(join(TEST_FILES_DIRECTORY, f))]

# print(test_file_names)
test_results = {}
for test_name in test_file_names:
    test_song = extract_data_from_file(TEST_FILES_DIRECTORY + test_name)
    gen = Genetic(test_song)
    final_guessed_population = gen.run(300)
    test_results[test_name] = final_guessed_population

print(test_results)
with open('test_results', 'wb') as f:
    pickle.dump(test_results, f)
