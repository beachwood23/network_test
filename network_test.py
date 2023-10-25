from matplotlib import pyplot as plt 
import matplotlib.dates as dateplot
import matplotlib.cbook as cbook
from matplotlib.ticker import MaxNLocator
import numpy
from datetime import datetime
import re
import os, sys
import time # for sleeping
import platform # for getting the operating system name
import subprocess # for executing a shell command
import asyncio # for executing async shell command
from tqdm import tqdm # progress indicator
import argparse

## accept user args for:
# duration in seconds
# host name of server running this script
# target server name
# target server network address (IP or FQDN)
def set_args():
	arg_parser = argparse.ArgumentParser(description = 'Creates charts from output of network pings.')

	arg_parser.add_argument(
		'-d',
		'--duration',
		help='The duration, in seconds, to run the network test for.',
		type=int,
		required=True)

	arg_parser.add_argument(
		'-n',
		'--name',
		help='The name of this host running the network test.',
		type=str,
		required=True)
	arg_parser.add_argument(
		'-t',
		'--target',
		help = 'The target host of the ping connections. Either IP or FQDN.',
		type = str,
		required=True)
	arg_parser.add_argument(
		'--nochart',
		help = 'If this flag is set, no chart will be generated.',
		required = False)

	return arg_parser

###
#  kick off ping test
###
def start_ping_test(duration, target, result_file):
	# Below code is borrowed from: https://stackoverflow.com/a/32684938
	# Option for the number of packets as a function of
	ping_cmd_param = '-n' if platform.system().lower()=='windows' else '-c'

	ping_loop_cmd = 'ping %s %s %s | while read pong;' % (ping_cmd_param, duration, target)
	ping_loop_cmd = ping_loop_cmd + ' do echo' + ' "$(date +%Y-%m-%d:%H:%M:%S): $pong"'
	ping_loop_cmd = ping_loop_cmd + ' >> %s ; done' % (result_file)

	# Original subprocess call - this works fine
	result = subprocess.call(ping_loop_cmd, shell=True)

###
# Display progress bar
###
def display_progress_bar(duration):
	## Using tqdm
	for i in tqdm(
				range(duration),
				unit='ping',
				desc='Network test progress',
				unit_scale=True):
		time.sleep(1)

###
# Wrap pings in async, display progress bar
###
async def run_ping_test(duration, target, result_file):
	# Because the 'ping' and 'tqdm' command has blocking i/o, it will block the task
	# from updating. We use asyncio.to_thread (new in python 3.9) to avoid.

	await asyncio.gather(
		asyncio.to_thread(display_progress_bar, duration),
		asyncio.to_thread(start_ping_test, duration, target, result_file))

###
#  generate charts
###
def generate_chart(name, target, result_file):
	test_results = open(result_file)

	DATETIME_FORMAT = '%Y-%m-%d:%H:%M:%S'
	ping_timestamps = []
	ping_responsetimes_ms = []

	## Read results file
	test_results.seek(0)
	for line in test_results:
		if 'from' in line:
			if platform.system().lower()=='windows':
				ping_timestamps.append(datetime.strptime(line[:line.index(': Reply') - 10], DATETIME_FORMAT))
				ping_responsetimes_ms.append(int((line[line.index('time') + 5:line.index('ms')])))
			else:
				ping_timestamps.append(datetime.strptime(line[:line.index('from') - 11], DATETIME_FORMAT))
					
				ping_responsetimes_ms.append(float((line[line.index('time') + 5:line.index('ms')])))

	test_results.close() # close results file

	## Prepare chart
	x_dates = dateplot.date2num(ping_timestamps)

	figure, axis = plt.subplots(figsize=(20, 5))
	axis.set(
		xlabel='Time of ping', 
		ylabel='Ping response time (ms)', 
		title='Ping latency from ' + name + ' to ' + target)
	axis.xaxis.set_major_locator(dateplot.HourLocator(interval=5))

	## Set the date format. We get this from:
	# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
	# Our format is like: Thu, Dec 10 2:00PM
	date_format = dateplot.DateFormatter("%a %b %d %I:%M%p")

	axis.xaxis.set_major_formatter(date_format)
	plt.xticks(rotation=20)
	axis.plot(ping_timestamps, ping_responsetimes_ms)

	axis.set_ylim(bottom=0,top=None) # get the y axis to start at 0

	plt.tight_layout() # get rid of cropped x-axis labels
	# chart_filename = 'chart-' + name + '-to-' + target + '.png'
	# figure.savefig(chart_filename)

	plt.show() # Enable this to show a preview of the chart for each one generated.


###
#  save charts to file, offer to display chart
###

if __name__ == '__main__':
	# Sets user arguments, then calls the class method to parse.
	args = set_args().parse_args()

	# Creates a result file timestamped with current date and time as a string in the format YYYYMMDD_HHMMSS
	result_file = 'result-%s-to-%s-%s.txt' % (args.name, args.target, datetime.now().strftime('%Y%m%d_%H%M%S'))

	print('Results will be saved to this file: %s' % result_file)
	print('To stop the test, press Ctrl-C until the test stops.')
	if not args.nochart:
		print('A chart will be generated at the end of the test. You can save the chart, or use the generate_chart() function after a series of tests to recover.')

	asyncio.run(run_ping_test(args.duration, args.target, result_file))

	if not args.nochart:
		print('Generating chart...')
		generate_chart(args.name, args.target, result_file)
