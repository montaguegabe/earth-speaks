from os import listdir
from os.path import isfile, join
import datetime

# For map-reduce
def flatten_generator(lol):
    for list2 in lol:
        for item in list2:
            yield item

class Logger(object):
    def __init__(self, fname):
        super(Logger, self).__init__()
        self.fname = fname
        self.log = open(fname, 'a')

    def __call__(self, str2):
        print(str2)
        self.log.write(datetime.datetime.now().isoformat() + ': ' + str2 + '\n')
     
# Returns a logging function that will write to the file specified   
def get_logger(fname):
    return Logger(fname)

# Makes a string usable as a file name
def make_fname_safe(filename):
    return ''.join([c for c in filename if c.isalpha() or c.isdigit()]).rstrip()
