#! /usr/bin/env python
# retrieve_vis04_data.py

import formatter
# import htmllib
import html.parser
import os
import re
import string
# import urllib
import urllib3
import requests


def _attrs2dict(attrs):
    """Take an (attribute, value) list and make a dict"""
    dict = {}
    for (a,v) in attrs:
        dict[a] = v
    return dict

class FileList(html.parser.HTMLParser):
    """Logic to retrieve the first page which lists the files, then return the files' URLs for retrieval"""
    base_url = 'http://www.vets.ucar.edu/vg/isabeldata/'
        
    def __init__(self, save_dir, match_string='*', debug=False):
        # htmllib.HTMLParser.__init__(self, formatter.NullFormatter())
        html.parser.HTMLParser.__init__(self, formatter.NullFormatter())
        self.match = re.compile(match_string)
        self.save_dir = save_dir
        self.debug = debug

    def do_it(self):

        # u = urllib3.PoolManager().request('GET', self.base_url)
        u = requests.get(self.base_url)
        self.feed(str(u.content))
        
    def start_a(self, attrs):
        """We're looking for links to .gz files"""
        d = _attrs2dict(attrs)
        link = d.get('href', ' ')
        if len(link) >= 3 and link[-3:] == '.gz':
            m = self.match.search(link)
            if m:
                #Found a matching file.
                #Get the file name for saving
                fn = os.path.split(link)[1]
                print('getting ' + link + ' to ' + self.save_dir)
                if not self.debug:
                    try:
                        urllib.urlretrieve(self.base_url + link, os.path.join(self.save_dir, fn))
                    except Exception as e:
                        print('-- failure:  ' + str(e))

if __name__ == '__main__':
##    f = FileList('h:/sources/python/testdata', 'CLOUDf1[2-4].*')
    import sys
    if len(sys.argv) < 3:
        print("Usage:  {-d} save_dir matching_string (which is a regular expression)")
    else:
        if sys.argv[1] == '-d':
            debug = True
            dir = sys.argv[2]
            match = sys.argv[3]
        else:
            debug = False
            dir = sys.argv[1]
            match = sys.argv[2]            
        f = FileList(dir, match, debug)
        f.do_it()    