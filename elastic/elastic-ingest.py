# We wish to upload JSON files to elastic

LOG_FNAME = 'elastic-ingest.log'
DATA_DIR = '../data/nasa/data-html/'

REVISION_NUM = 1
NUM_CHUNKS = 2048

HOST = 'search-e5ud2nsmhsp52orvyvpqur0k09x-bkkbyr2hfjeiyujryuqkm5y3hu.us-east-1.es.amazonaws.com'
PORT = 443
TARGET_INDEX = 'nature-english'
DOC_TYPE = 'paper'

import os
import sys
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from os import listdir
from os.path import isfile, join
import mining.util
from cleaning.nature.convert import file2doc

from elasticsearch import Elasticsearch
from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk

from joblib import Parallel, delayed
import multiprocessing


file_list = [f for f in listdir(DATA_DIR) if isfile(join(DATA_DIR, f))]
chunk_size = int(len(file_list) / NUM_CHUNKS) + 1
chunks = [file_list[i:i + chunk_size] for i in xrange(0, len(file_list), chunk_size)]
print('MAX_CHUNK: %d' % len(chunks))

START_CHUNK = int(raw_input('START_CHUNK: '))
END_CHUNK = int(raw_input('END_CHUNK: ')) # (exclusive)

# Set up logging
from common import get_logger
writelog = get_logger(LOG_FNAME)

writelog('Starting Elasticsearch ingestion...')
writelog('START_CHUNK: ' + str(START_CHUNK))
writelog('END_CHUNK: ' + str(END_CHUNK))

# Turns a chunk of files into docs while bulk ingesting
def mapingest_chunk(chunk):

    # Set up ES
    es = Elasticsearch(
        hosts=[{'host': HOST, 'port': PORT}],
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    es.info()

    docs = []
    errors = []
    for fname in chunk:
        (err, docs_small) = file2doc(fname)
        errors.append(err)
        docs.extend(docs_small)

    # Ingest all docs
    resp = bulk(es, docs, stats_only=True, index=TARGET_INDEX, doc_type=DOC_TYPE)

    return (errors, docs, resp)

#print 'Chunks:'
#for chunk in chunks:
#    print len(chunk)

target_chunks = chunks[START_CHUNK:END_CHUNK]

# Map
num_cores = multiprocessing.cpu_count()
print 'Cores:', num_cores
results = Parallel(n_jobs=num_cores)(delayed(mapingest_chunk)(i) for i in target_chunks)

# Reduce while writing errors
for result in results:
    (errors, docs, resp) = result

    for error in errors:
        if error != None:
            print('ERROR: ' + str(error))

    writelog('Success/failure: (%d, %d)' % (resp[0], resp[1]))

writelog('Ingestion complete')
