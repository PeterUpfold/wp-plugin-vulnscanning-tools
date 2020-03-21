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
import argparse
import os


# argument parsing
argparser = argparse.ArgumentParser(description='Determine which WordPress plugins interest us.')
argparser.add_argument('-i', '--input', dest='inputfile', help='The input index.html file from plugins.svn.wordpress.org.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputpath', help='The directory for the output files', required=True)
argparser.add_argument('--force', dest='force', help='Allow this script to overwrite files in the output folder.', action='store_true')

args = argparser.parse_args()

if not os.path.exists(args.inputfile):
    raise ValueError("Input HTML file does not exist.")


# * for each top level plugin slug, pull the https://wordpress.org/plugins/{name} page and parse number of installations
# * Decide which plugins to target based on user base

class RootSVNPageParser(HTMLParser):
    def __init__(self):
        super().__init__()

    def handle_starttag(self, tag, attrs):
        print("Start ", tag)

    def handle_endtag(self, tag):
        print ("end", tag)

    def handle_data(self, data):
        pass

svn_page_parser = RootSVNPageParser()

svn_page_parser.feed(args.inputfile.read())