#!/usr/bin/env python3
"""
Generate summary reports for the performances.
"""
import argparse
import csv
import os
import re
import time

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


def read_file(path, summary, errors):
    run_time = None
    with open(path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[0] == 'REQUEST':
                _, _, _, group, level, start, stop, status, _ = row
                group = group.split(',') + [level]
                if status == "OK":
                    time = int(stop) - int(start)
                    merge_dict(summary, group, time)
                else:
                    merge_dict(errors, group, 1)
            elif row[0] == 'RUN':
                run_time = 1501754177650
    return run_time


def gen_csv(filename, summary, errors):
    with open(filename, "w") as dest:
        writer = csv.writer(dest, delimiter='\t')
        writer.writerow(['nb_users', 'server', 'layer', 'level', 'nb', 'avg_ms'])
        flatten_dict(summary, [], lambda cols: writer.writerow(cols))
        writer.writerow([])
        writer.writerow([])
        writer.writerow(['Errors'])
        writer.writerow(['nb_users', 'server', 'layer', 'level', 'nb', 'one'])
        flatten_dict(errors, [], lambda cols: writer.writerow(cols))
    print("CSV summary report available here: " + filename)


def gen_html(filename, summary, errors, run_time):
    servers = set()
    levels = set()
    for nb_users, per_user in summary.items():
        servers.update(per_user.keys())
        for server, per_server in per_user.items():
            for layer, per_layer in per_server.items():
                levels.update(per_layer.keys())
    servers = sorted(servers)
    levels = sorted(levels)

    # convert the data in the good format:
    # {nb_users: {server: {layer: {level: [nb, avg_ms]}}}} => {layer: {level: {nb_users: [avg_ms_server1, ...]}}}
    data = {}
    for nb_users, per_user in summary.items():
        for server, per_server in per_user.items():
            for layer, per_layer in per_server.items():
                for level, stats in per_layer.items():
                    data.setdefault(layer, {}).setdefault(level, {}).setdefault(nb_users, [0] * len(servers))[servers.index(server)] = stats[1]/stats[0]

    with open(filename, "w") as html:
        html.write("""
<html>
  <head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawCharts);

      function filterLevel(level) {""")
        for level in levels:
            html.write('      var elems = document.getElementsByClassName("level_%(level)s");\n' % {'level': level})
            html.write('      for (var i = 0; i < elems.length; i++) elems[i].style.display = ((level === %(level)s || level === "all") ? "block" : "none");\n' % {'level': level})
        html.write("""
      }

      function drawCharts() {
        var options = {
          hAxis: {title: 'Nb users', minValue: 1},
          vAxis: {title: 'Render time [ms]', minValue: 0},
          legend: 'right',
          lineWidth: 2,
        };

        """)

        for layer, per_layer in data.items():
            for level, per_level in per_layer.items():
                html.write("""
        var data = google.visualization.arrayToDataTable([
          ['Nb users', '%(columns)s']""" % {'columns': "','".join(servers)})
                for nb_users, per_nb in sorted(per_level.items()):
                    html.write("\n         ,[%s, %s]" % (nb_users, ",".join(map(lambda x: str(x) if x > 0.0 else 'null', per_nb))))
                html.write("""
        ]);

        var chart = new google.visualization.ScatterChart(document.getElementById('chart_div_%(layer)s_%(level)s'));

        chart.draw(data, options);
                """ % {'layer': layer, 'level': level})

        html.write("""
      }
    </script>
  </head>
  <body>
    <h1>Cartographic servers performances</h1>
        """)
        html.write('Filter by level: <a href="javascript:filterLevel(\'all\')">all</a> ' % {'level': level})
        for level in levels:
            html.write('<a href="javascript:filterLevel(%(level)s)">%(level)s</a> ' % {'level': level})
        for layer, per_layer in sorted(data.items()):
            html.write("    <h2>Layer: %s</h1>\n" % layer)
            for level, per_level in sorted(per_layer.items()):
                html.write('      <h3 class="level_%(level)s">Level: %(level)s</h2>\n' % {'level': level})
                html.write('        <div class="level_%(level)s" id="chart_div_%(layer)s_%(level)s" style="width: 100%%; height: 500px;"></div>\n' % {'layer': layer, 'level': level})
        html.write("""
    <p align="right">Generate on %(run_time)s</p>
  </body>
</html>
        """ % {'run_time': time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.localtime(run_time/1000))})
    print("HTML summary report available here: " + filename)

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', default=None, help="The CSV file to generate")
    parser.add_argument('--html', default=None, help="The HTML file to generate")
    return parser.parse_args()


def main():
    args = parse_args()
    summary = {}
    errors = {}
    run_time = None
    for dirname in os.listdir(BASE_PATH):
        if FILE_RE.match(dirname):
            run_time = read_file(os.path.join(BASE_PATH, dirname, 'simulation.log'), summary, errors)

    if args.csv is not None:
        gen_csv(args.csv, summary, errors)
    if args.html is not None:
        gen_html(args.html, summary, errors, run_time)

main()
