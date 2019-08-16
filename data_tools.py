__all__ = ('save_dataset', 'load_dataset')
import pickle


def save_dataset(dataset):
    in_file = open('dataset.txt', 'w')
    pickle.dump(dataset, in_file)
    in_file.close()


def load_dataset():
    out_file = open('dataset.txt', 'r')
    dataset = pickle.load(out_file)
    out_file.close()
    return dataset