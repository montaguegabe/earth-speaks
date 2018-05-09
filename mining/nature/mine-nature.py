# Parameters
LOG_FNAME = 'mining.log'
DATA_DIR = '../../data/nature/data-html/' # you may have to create this
CREDENTIALS_FILE = '../../credentials/nature.json'

DEFAULT_PAGESIZE = 25
DEFAULT_KWS = ['climate', 'earth']

import os
import sys
module_path = os.path.abspath('../..')
if module_path not in sys.path:
    sys.path.append(module_path)

from mining import util
from common import get_logger
import datetime
import requests

# Set up logging
writelog = get_logger(LOG_FNAME)

# Get keywords to extract
raw = input('Which keywords? (sep. with comma, default: %s)' % ','.join(DEFAULT_KWS))
if len(raw) == 0:
    keywords = DEFAULT_KWS
else:
    keywords = raw.split(',')

# Get starting index
raw = input('Enter starting index (default 1)')
record_index = None
if len(raw) == 0:
    record_index = 1
else:
    record_index = int(raw)

writelog('Searching with keywords %s, starting at index %d' % (keywords, record_index))

# Form query
search_include = map(lambda str2: 'cql.keywords any ' + str2, keywords)
search_filter = [
    # (We apply this filter to be able to get the full HTML of each)
    'dc.publisher=Nature Publishing Group'
]
cql_query = '(' + ' OR '.join(search_include) + ') AND ' + ' AND '.join(search_filter)
#print 'Query:', cql_query

url = 'http://api.nature.com/content/opensearch/request'

total_records = None

# Loop through pages
while True:
    data = {
        'httpAccept': 'application/json',
        'queryType': 'cql',
        'startRecord': str(record_index),
        'query': cql_query
    }
    try:
        response = requests.get(url, params=data)
    except requests.exceptions.RequestException as e:
        writelog(str(e))
        continue

    body = response.json()

    if total_records == None:
        total_records = body['feed']['sru:numberOfRecords']
        writelog('Found a total of %d records' % (total_records))

    # Process each entry
    entries = body['feed']['entry']
    for entry in entries:

        doi = entry['id']
        writelog('Record index: %d, DOI: %s' % (record_index, doi))

        entry_url = entry['link']

        # Get the redirected page
        try:
            response = requests.get(entry_url)
        except requests.exceptions.RequestException as e:
            writelog(str(e))
            continue
        
        redirected_url = response.url

        # Build the URL of the HTML page with the full article
        doc_id = redirected_url.split('/')[-1]
        article_url_fmt = 'http://www.nature.com.ezp-prod1.hul.harvard.edu/articles/%s'
        article_url = article_url_fmt % doc_id
        
        cookies = util.get_cookies(CREDENTIALS_FILE)
        try:
            article_fname = util.download_file(article_url, cookies, prefix=DATA_DIR + '/')
        except Exception as e:
            writelog(str(e))
            continue

        # Check if something went wrong
        ext = article_fname.split('.')[-1]
        if ext == 'pdf' or ext == 'html':
            writelog('Detected error, deleting..')
            os.remove(join(DATA_DIR, article_fname))

        record_index += 1

    # Check if we should exit
    if body['feed']['opensearch:itemsPerPage'] < DEFAULT_PAGESIZE:
        break

    # Set the next record index
    record_index = int(body['feed']['sru:nextRecordPosition'])

writelog('Query download completed')

