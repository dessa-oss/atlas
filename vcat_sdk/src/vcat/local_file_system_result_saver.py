class LocalFileSystemResultSaver(object):

    def save(self, name, results):
        import pickle

        file_name = name + ".pkl"
        with open(file_name, 'w+b') as file:
            pickle.dump(results, file)
