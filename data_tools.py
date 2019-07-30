__all__ = ('save_dataset', 'load_dataset')
import pickle

dataset = {249260525: [None, 'encrypt', None, 'Kirill', '@Kiryao', 'encrypt'], 598721158: [
    None, 'encrypt', None, 'Margaret', '@m_mckey', 'encrypt']}


def save_dataset(dataset):
    with open('dataset.txt', 'wb') as out_put:
        pickle.dump(dataset, out_put)


def load_dataset():
    with open('dataset.txt', 'rb') as in_put:
        dataset = pickle.load(in_put)
    return dataset