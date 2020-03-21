#!/usr/bin/env python3
#
#
#
# Determine which WordPress plugins interest us
#
#
#
# Copyright 2020 Peter Upfold.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from html.parser import HTMLParser
import lxml # don't ask me why I'm parsing HTML two different ways. I had some existing code, all right? :)
import argparse
import os
import re
import requests
from time import sleep


# argument parsing
argparser = argparse.ArgumentParser(description='Determine which WordPress plugins interest us.')
argparser.add_argument('-i', '--input', dest='inputfile', help='The input index.html file from plugins.svn.wordpress.org.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputpath', help='The directory for the output files', required=True)
argparser.add_argument('--force', dest='force', help='Allow this script to overwrite files in the output folder.', action='store_true')

args = argparser.parse_args()

headers = {'User-Agent', 'determine-target-plugins.py +https://github.com/PeterUpfold/wp-plugin-vulnscanning-tools/'}

# * for each top level plugin slug, pull the https://wordpress.org/plugins/{name} page and parse number of installations
# * Decide which plugins to target based on user base

class RootSVNPageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.slug_regex = re.compile(r'^((\w)*(\-)*)*/$')
        self.slugs = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            slug = attrs[0][1]
            self.slugs.append(slug)

            # the regex causes huge slowdowns ~>12,500 items. No idea why...
            #if self.slug_regex.search(slug):
            #    print('Adding slug ', slug)
            #    self.slugs.append(slug)

    def handle_endtag(self, tag):
        #print ("end", tag)
        pass

    def handle_data(self, data):
        pass


svn_page_parser = RootSVNPageParser()

svn_page_parser.feed(args.inputfile.read())

plugins = {} # store our overall state

for slug in svn_page_parser.slugs:
    # go get the plugin page. We'll need to pull the number of installs
    print('Pulling page for ', slug)

    plugin_page = requests.get('https://wordpress.org/plugins/' + slug + '/', headers=headers)
    if plugin_page.status_code == 200:
        tree = lxml.html.fromstring(plugin_page.content)
        installs = tree.xpath('/html/body/div[3]/div/main/article/div[3]/div[1]/ul/li[3]/strong/text()')

        print(slug + ' has ' + installs)
    else:
        print('Failed on ' + slug + ' with error ' + str(plugin_page.status_code))


    print('Finished with ', slug)
    sleep(3) # robots.txt for plugins.svn.wordpress.org indicates this
