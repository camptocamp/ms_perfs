#!/usr/bin/env python3
"""
Generate summary reports for the performances.
"""
import argparse
import csv
import os
import re
import time
import json
from collections import namedtuple

BASE_PATH = 'perfs/results'
FILE_RE = re.compile(r'test-.*')

stat = namedtuple('record', ['successes', 'errors', 'time'])


def add_request(dict_, groups, success, time):
    if len(groups) == 1:
        key = groups[0]
        v = dict_.get(key, stat(0, 0, 0.0))
        if success:
            dict_[key] = stat(v.successes + 1,
                              v.errors,
                              v.time + time)
        else:
            dict_[key] = stat(v.successes,
                              v.errors + 1,
                              v.time)
    else:
        add_request(dict_.setdefault(groups[0], {}), groups[1:], success, time)


def flatten_dict(dico, row, callback):
    for key, value in dico.items():
        sub_row = row + [key]
        if isinstance(value, dict):
            flatten_dict(value, sub_row, callback)
        else:
            requests = value.errors + value.successes
            avg_time = round(value.time / value.successes, 2) if value.successes > 0 else None
            percent_errors = value.errors / requests if requests else None
            values = sub_row + [
                value.successes,
                avg_time or '',
                '{0:.0%}'.format(percent_errors)]
            callback(values)


def read_file(path, summary):
    run_time = None
    with open(path, 'r') as file:
        print('reading %s' % path)
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            if row[0] == 'REQUEST':
                _, _, _, group, level, start, stop, status, _ = row
                groups = group.split(',') + [level]
                add_request(summary, groups, status == 'OK', int(stop) - int(start))
            elif row[0] == 'RUN':
                run_time = int(row[4])
    return run_time


def gen_csv(filename, summary):
    with open(filename, "w") as dest:
        writer = csv.writer(dest, delimiter='\t')
        writer.writerow(['nb_users', 'server', 'layer', 'level', 'successes', 'avg_ms', 'errors'])
        flatten_dict(summary, [], lambda cols: writer.writerow(cols))
    print("CSV summary report available here: " + filename)


def gen_html(filename, summary, run_time):
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
                    data. \
                        setdefault(layer, {}). \
                        setdefault(int(level), {
                            'avg_times': {},
                            'errors': {}
                        })

                    avg_times = stats.time / stats.successes if stats.successes else None
                    data[layer][int(level)]['avg_times']. \
                        setdefault(int(nb_users), [0] * len(servers))[servers.index(server)] = avg_times

                    requests = stats.successes + stats.errors
                    errors = stats.errors / requests if requests else None
                    data[layer][int(level)]['errors']. \
                        setdefault(int(nb_users), [0] * len(servers))[servers.index(server)] = errors

    with open(filename, "w") as html:
        html.write("""
<html>
  <head>
    <link href="style.css" rel="stylesheet">
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawCharts);

      function filterLevel(level) {""")
        for level in levels:
            html.write("""
        var elems = document.getElementsByClassName("level_%(level)s");
        for (var i = 0; i < elems.length; i++)
          elems[i].style.display = ((level === %(level)s || level === "all") ? "block" : "none");""" % {'level': level})
        html.write("""
      }

      function hidableSeries(chart, data, options) {
        var visible_columns = [];
        var columns = [];
        var series = {};
        for (var i = 0; i < data.getNumberOfColumns(); i++) {
          visible_columns.push(true);
          columns.push(i);
          if (i > 0) {
            series[i - 1] = {};
          }
        }

        google.visualization.events.addListener(chart, 'select', function () {
          var sel = chart.getSelection();
          // if selection length is 0, we deselected an element
          // if row is undefined, we clicked on the legend
          if (sel.length > 0 && sel[0].row === null) {
            var col = sel[0].column;
            visible_columns[col] = !visible_columns[col];
            for (var i = 1; i < data.getNumberOfColumns(); i++) {
              if (visible_columns[i]) {
                columns[i] = i;
                series[i - 1] = {};
              }
              else {
                columns[i] = {
                  label: data.getColumnLabel(i),
                  type: data.getColumnType(i),
                  calc: function () {
                    return null;
                  }
                };
                // grey out the legend entry
                series[i - 1].color = '#CCCCCC';
              }
            }

            var view = new google.visualization.DataView(data);
            view.setColumns(columns);
            options.series = series;
            chart.draw(view, options);
          }
        });
      }

      function drawCharts() {
        function merge_options(obj1,obj2){
          var obj3 = {};
          for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; }
          for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; }
          return obj3;
        }

        var common_options = {
          width: 800,
          height: 300,
          chartArea:{
            left: 100,
            top: 50,
            width: 550,
            height: 200
          },
          hAxis: {
            title: 'Number of users',
            scaleType: 'log'
          },
          legend: 'right',
          lineWidth: 2
        };

        var options_avg_times = merge_options(common_options, {
          title: 'Average response time',
          vAxis: {
            title: 'Render time [ms]',
            minValue: 0
          }
        });

        var options_errors = merge_options(common_options, {
          title: 'Percentage of failures',
          vAxis: {
            title: 'Percentage of errors',
            minValue: 0,
            format:'#,###%'
          }
        });

        """)

        for layer, per_layer in data.items():
            for level, per_level in per_layer.items():
                html.write("""
        var data_%(layer)s = new google.visualization.DataTable();
        data_%(layer)s.addColumn('number', 'Nb users');""" % {'layer': layer})
                for server in servers:
                    html.write("""
        data_%(layer)s.addColumn('number', '%(server)s');""" % {'layer': layer, 'server': server})
                html.write("""
        data_%(layer)s.addRows(""" % {'layer': layer});
                html.write("""
        """.join(
                    json.dumps([
                        [nb_users] + avg_times
                        for nb_users, avg_times in sorted(per_level['avg_times'].items())
                    ], indent=4).splitlines()
                ))
                html.write(""");

        var chart_%(layer)s = new google.visualization.ScatterChart(
            document.getElementById('chart_div_%(layer)s_%(level)s_avgtimes'));
        chart_%(layer)s.draw(data_%(layer)s, options_avg_times);
        hidableSeries(chart_%(layer)s, data_%(layer)s, options_avg_times);
                """ % {'layer': layer, 'level': level})


                html.write("""
        var data_%(layer)s_errors = new google.visualization.DataTable();
        data_%(layer)s_errors.addColumn('number', 'Nb users');""" % {'layer': layer})
                for server in servers:
                    html.write("""
        data_%(layer)s_errors.addColumn('number', '%(server)s');""" % {'layer': layer, 'server': server})
                html.write("""
        data_%(layer)s_errors.addRows(""" % {'layer': layer});
                html.write("""
        """.join(
                    json.dumps([
                        [nb_users] + errors
                        for nb_users, errors in sorted(per_level['errors'].items())
                    ], indent=4).splitlines()
                ))
                html.write(""");

        var chart_%(layer)s_errors = new google.visualization.ScatterChart(
            document.getElementById('chart_div_%(layer)s_%(level)s_errors'));
        chart_%(layer)s_errors.draw(data_%(layer)s_errors, options_errors);
        hidableSeries(chart_%(layer)s_errors, data_%(layer)s_errors, options_errors);
                """ % {'layer': layer, 'level': level})
        html.write("""
      }
    </script>
  </head>
  <body>
    <h1>Cartographic servers performances</h1>
    Filter by level: <a href="javascript:filterLevel(\'all\')">all</a>""" % {'level': level})
        for level in levels:
            html.write("""
    <a href="javascript:filterLevel(%(level)s)">%(level)s</a>""" % {'level': level})
        for layer, per_layer in sorted(data.items()):
            html.write("""

    <h2>Layer: %s</h2>""" % layer)
            for level, per_level in sorted(per_layer.items()):
                html.write("""

    <h3 class="level_%(level)s">Level: %(level)s</h3>""" % {'level': level})
                html.write("""
    <div class="chart avgtime level_%(level)s" id="chart_div_%(layer)s_%(level)s_avgtimes"></div>""" % {'layer': layer, 'level': level})
                html.write("""
    <div class="chart errors level_%(level)s" id="chart_div_%(layer)s_%(level)s_errors"></div>""" % {'layer': layer, 'level': level})
        html.write("""

    <p align="right">Generate on %(run_time)s</p>
  </body>
</html>
""" % {'run_time': time.strftime('%a, %d %b %Y %H:%M:%S +0000', time.localtime(run_time/1000))})
    print("HTML summary report available here: " + filename)

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prefix', default=None, help="The prefix of the files to generate")
    parser.add_argument('--csv', default=False, action='store_true', help="Generate the CSV file")
    parser.add_argument('--html', default=False, action='store_true', help="Generate the HTML file")
    return parser.parse_args()


def main():
    args = parse_args()
    summary = {}
    run_time = None
    for dirname in os.listdir(BASE_PATH):
        if FILE_RE.match(dirname):
            run_time = read_file(os.path.join(BASE_PATH, dirname, 'simulation.log'), summary)

    day = time.strftime('%Y-%m-%d', time.localtime(run_time/1000))

    prefix = args.prefix + day
    if args.csv:
        gen_csv(prefix + '.csv', summary)
    if args.html:
        gen_html(prefix + '.html', summary, run_time)

main()
