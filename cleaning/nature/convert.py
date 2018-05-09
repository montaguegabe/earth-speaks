# File for converting raw Nature data to other formats

import os
import sys
module_path = os.path.abspath(os.path.join('../..'))
if module_path not in sys.path:
    sys.path.append(module_path)

from bs4 import BeautifulSoup
import re
from common import make_fname_safe

# Certain sections contain useless information
SKIP_SECTIONS = set([
    'acknowledgements',
    'references',
    'author-information',
    'supplementary-information',
    'article-comments'
])

# We define a method that turns HTML into text
# Source: https://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python
def html2txt(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Kill all script, style, and link elements
    for script in soup(['script', 'style', 'a', 'h2']):
        script.extract()    # rip it out
        
    # Get text
    text = soup.get_text()

    return text

def is_number(s):
    return s[0].isdigit()

# Does preprocessing on a file and returns status
def file2doc(fname):
    try:
        doc = {}

        html = None
        with open(fname, 'r', encoding='utf-8') as example_html:
            html = example_html.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Find article date and title
        date_el = soup.find('time')
        title_el = soup.find('h1', {'data-article-title': re.compile(r".*")})
        title = html2txt(str(title_el))
        date_str = html2txt(str(date_el))
        try:
            date = dateutil.parser.parse(date_str)
        except Exception as e:
            date = None
        doc['article_title'] = title
        doc['article_date'] = date

        # Find article sections
        sections = soup.findAll('section', {'aria-labelledby': re.compile(r".*")})

        # Extract each to text
        s_count = 0
        for section in sections:
            
            # Skip useless sections
            s_title = section['aria-labelledby']
            if s_title in SKIP_SECTIONS:
                continue
            
            # Otherwise we turn the section into plain text
            text = html2txt(str(section))
            text = re.sub(r'[^\x00-\x7f]',r' ', text) # remove non-unicode
            s_count += 1

            # Create doc
            doc = {}
            s_title
            doc[s_title] = text

        if s_count == 0:
            raise ValueError('No sections')

    except Exception as e:
        return (e, [])
    else:
        return (None, doc)