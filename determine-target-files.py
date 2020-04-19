#!/usr/bin/env python3
#
#
#
# Determine PHP files
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

from bs4 import BeautifulSoup
import requests
import json
import signal
import sys
import argparse

# argument parsing
argparser = argparse.ArgumentParser(description='Determine which WordPress plugin PHP files interest us.')
argparser.add_argument('-i', '--input', dest='inputfile', help='The input target-plugins.json file.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputfile', help='The target-files.json file.', required=True)
argparser.add_argument('-p', '--position', dest='positionfile', help='The file to record our current plugin position', required=True)
argparser.add_argument('--force', dest='force', help='Allow this script to overwrite files in the output folder.', action='store_true')

args = argparser.parse_args()

headers = {'User-Agent': 'determine-target-files.py +https://github.com/PeterUpfold/wp-plugin-vulnscanning-tools/'}
php_file_list = []

current_position = json.load(open(args.positionfile, 'r'))
current_plugin = ''

with open(args.outputfile, 'r') as output:
    php_file_list = json.load(output)

print(php_file_list)

def sigint_handler(signal, frame):
    # dump current file list and start position

    with open(args.outputfile, 'w') as output:
        output.write(json.dumps(php_file_list))

    with open(args.positionfile, 'w') as position:
        position.write(json.dumps({'current_plugin': current_plugin }))

    
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

def process_tree(url):
    global current_plugin
    global php_file_list
    page = requests.get(url, headers=headers)

    # split url and gather plugin slug
    current_plugin = url.split('/')[3]
    print('==> Current plugin: ' + current_plugin)

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all('a'):
           if not link.get('href').startswith('http') and not link.get('href').startswith('.'): # this is hacky
               # if url ends in /
               if link.get('href').endswith('/'):
                   print('recurse into ' + link.get('href'))
                   process_tree(url + link.get('href'))
               # if url ends in .php
               elif link.get('href').endswith('.php'):
                   php_file_list += [url + link.get('href')]
           else:
               if not link.get('href').startswith('.'):
                   print('Unexpected link on ' + url + '. Link was ' + link.get('href'))
    else:
        print('Failed on ' + url + ' with error ' + str(page.status_code))

plugins = json.load(args.inputfile)

for plugin in plugins:
    process_tree('https://plugins.svn.wordpress.org/' + plugin + '/trunk/')

sigint_handler(None, None)