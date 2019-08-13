__all__ = ('save_dataset', 'load_dataset')
import pickle


def save_dataset(dataset):
    with open('dataset.txt', 'wb') as out_put:
        pickle.dump(dataset, out_put)


def load_dataset():
    with open('dataset.txt', 'rb') as in_put:
        dataset = pickle.load(in_put)
    return dataset