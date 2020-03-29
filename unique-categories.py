#!/usr/bin/env python3
#
#
# Unique installs categories
#
#
import json

file = 'output/plugins-2020-03-22.json'
out_file = 'output/unique-categories.json'

with open(file, 'r') as openedfile:
    data = json.load(openedfile)

    uniques = set()

    for item in data.values():
        if not uniques.__contains__(item):
            uniques.add(item)


    for item in uniques:
        print(item)

    with open(out_file, 'w') as outfile:
        outfile.write(json.dumps(list(uniques)))