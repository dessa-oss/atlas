class LocalFileSystemFetcher(object):

    def fetch_results(self):
        import glob
        import pickle

        self.results = []
        file_list = glob.glob('*.pkl')
        for file_name in file_list:
            with open(file_name, 'rb') as file:
                self.results.append(pickle.load(file))
        return self.results
