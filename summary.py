#!/usr/bin/env python3
import csv
import os
import re

BASE_PATH = 'perfs/results'
FILE_RE = re.compile(r'test-.*')

def merge_dict(target, group, value):
    if len(group) == 1:
        old = target.get(group[0], [0, 0])
        target[group[0]] = [old[0] + 1, old[1] + value]
    else:
        merge_dict(target.setdefault(group[0], {}), group[1:], value)


def flatten_dict(dico, row, callback):
    for key, value in dico.items():
        sub_row = row + [key]
        if isinstance(value, dict):
            flatten_dict(value, sub_row, callback)
        else:
            callback(sub_row + [value[0], value[1]/value[0]])


def read_file(path, summary):
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[0] == 'REQUEST':
                _, _, _, group, level, start, stop, status, _ = row
                if status == "OK":
                    time = int(stop) - int(start)
                    group = group.split(',') + [level]
                    merge_dict(summary, group, time)
                else:
                    print("Error for " + "/".join(group))


def main():
    summary = {}
    for dirname in os.listdir(BASE_PATH):
        if FILE_RE.match(dirname):
            read_file(os.path.join(BASE_PATH, dirname, 'simulation.log'), summary)

    with open("summary.csv", "w") as dest:
        writer = csv.writer(dest, delimiter='\t')
        writer.writerow(['nb_users', 'server', 'layer', 'level', 'nb', 'avg_ms'])
        flatten_dict(summary, [], lambda cols: writer.writerow(cols))

main()
