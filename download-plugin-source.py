#!/usr/bin/env python3
#
#
#
# Download source of each target plugin
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
import subprocess
import os

with open('output/target-plugins.json', 'r') as plugins_list_file:
    plugins_list = json.load(plugins_list_file)

    try:
        os.makedirs("source")
    except OSError as err:
        print(err)

    for plugin in plugins_list:
        this_plugin_dir = os.path.join("source", plugin)
        if os.path.exists(this_plugin_dir):
            print("Skipping " + plugin + " as directory exists")
            continue

        os.makedirs(this_plugin_dir)

        result = subprocess.run(["svn", "co", "https://plugins.svn.wordpress.org/" + plugin], cwd="source")

        if result.returncode == 0:
            print("Checked out " + plugin)
        else:
            print("Failed to checkout " + plugin + " with return code " + str(result.returncode))
            if len(os.listdir(this_plugin_dir)) == 0:
                os.rmdir(this_plugin_dir)
            