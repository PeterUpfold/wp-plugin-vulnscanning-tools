#!/usr/bin/env python3
#
#
#
# Determine which WordPress plugins interest us from our list of data
# and our target categories
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


import json

with open('output/plugins-2020-03-22.json', 'r') as plugins_list:
    target_categories = []
    with open('output/target-categories.json', 'r') as target_categories_file:
        target_categories = json.load(target_categories_file)
    
    target_plugins = []
    for item in json.load(plugins_list).items():
        if item[1] in target_categories:
            target_plugins += [item[0][:-1]]

    with open('output/target-plugins.json', 'w') as target_plugins_list:
        target_plugins_list.write(json.dumps(target_plugins))
