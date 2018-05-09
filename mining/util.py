import os
import sys
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import requests
import re
from os.path import join
import json
import pyperclip, webbrowser

# Returns cookies from a file path
def get_cookies(fname):
    with open(fname, 'r') as f:
        json_str = f.read().replace('\n', '')
    return json.loads(json_str)

# Source: https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py

# Downloads file given cookies and URL
def download_file(url, cookies, prefix=''):

    local_filename = url.split('/')[-1]
    r = requests.get(url, cookies=cookies, stream=True)
    
    # Catch bad status codes
    if r.status_code != 200:
        raise RuntimeError('Credentials have expired')

    with open(join(prefix, local_filename), 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename

# Opens a browser window to view a JSON response
def browseJSON(json_str):
    pyperclip.copy(json_str)
    webbrowser.open_new_tab('https://jsonformatter.curiousconcept.com/')

def find_between(str2, before, after):
    result = re.search(before + '(.*)' + after, str2)
    if result == None:
        return None
    return result.group(1)