# An iterator to iterate over the contents of a directory. Still incompatible with gensim

from os import listdir
from os.path import isfile, join

# Define an iterator for streaming the pickle files
class DirectorySentenceIterator:
    def __init__(self, start, at_a_time, filedir, fname2sentences):
        self.batch_index = start # global index of start of batch
        self.at_a_time = at_a_time

        # fname2sentences should be a function that converts a file to sentences
        self.fname2sentences = fname2sentences
        
        # Get list of files in directory
        self.file_list = [f for f in listdir(filedir) if isfile(join(filedir, f))]

        self.batch = []
        self.filedir = filedir
        self.index = 0 # within the batch
        self.last = False
        self._update_batch()

    # Makes use of the current index to update the batch
    def _update_batch(self):

        self.batch = []
        
        end_ind = self.batch_index + self.at_a_time
        if end_ind >= len(self.file_list):
            end_ind = len(self.file_list)
            self.last = True
        batch_files = self.file_list[self.batch_index:end_ind]
        
        for fname in batch_files:
            sentences = fname2sentences(fname)
            self.batch.extend(sentences)
            
        if len(self.batch) == 0:
            if not self.last:
                self.batch_index += self.at_a_time
                self._update_batch()
            else:
                raise StopIteration
        
    def __iter__(self):
        return self

    def next(self):
        if self.index >= len(self.batch):
            if self.last:
                raise StopIteration
            else:
                self.index = 0
                self.batch_index += self.at_a_time
                self._update_batch()
        self.index += 1
        return self.batch[self.index - 1]
