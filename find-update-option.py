#!/usr/bin/env python3
#
#
#
# Find calls to update_option
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
argparser.add_argument('-i', '--input', dest='inputfile', help='The input target-files.json file.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputfile', help='.', required=True)
argparser.add_argument('-p', '--position', dest='positionfile', help='The file to record our current file position', required=True)

args = argparser.parse_args()

headers = {'User-Agent': 'find-update-option.py +https://github.com/PeterUpfold/wp-plugin-vulnscanning-tools/'}

file_list = json.load(args.inputfile)

current_url = ''
target_lines = []
current_index = 0

def sigint_handler(signal, frame):
    global current_index
    global current_url

    with open(args.outputfile, 'w') as output:
        output.write(json.dumps(target_lines, indent=4))

    with open(args.positionfile, 'w') as position:
        position.write(json.dumps({'current_url': current_url, 'index': current_index }, indent=4))

    print('===== Save position: ' + current_url + ' at ' + str(current_index))
    if signal is not None:
        sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

skip = 0
# load current position
with open(args.positionfile, 'r') as position:
    position_json = json.load(position)
    if 'index' in position_json:
        skip = position_json['index']

for file in file_list:
    if skip > 0:
        skip -= 1
        current_index += 1
        print('Skip ' + file + ' as already processed')
        continue

    page = requests.get(file, headers=headers)

    line_no = 0
    try:
        page_utf8 = page.content.decode('utf-8')
    except UnicodeDecodeError:
        print('Failed to decode ' + file)
        current_url = file
        current_index += 1
        continue

    for line in page_utf8.split('\n'):
        if 'update_option(' in line:
            target_lines += [{ 'url': file, 'line': line_no, 'line_content': line}]
            print('Found a target line in ' + file)
        line_no += 1
    
    current_url = file
    current_index += 1
    if current_index % 20 == 0:
        sigint_handler(None, None)

sigint_handler(None, None)