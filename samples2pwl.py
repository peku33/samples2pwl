# -*- coding: utf-8 -*-

import sys
import os
import re

samples_file_clock_regex = re.compile('#CLOCK=([\\d\\.]+)S')

# 
# Converts samples file contents to pwl file / string contents.
#
def samples_file_content_to_pwl_file_content(samples_file_contents):

	# Split samples file contents into lines
	samples_file_lines = samples_file_contents.splitlines()

	# Output variables

	# Clock period (None / float)
	clock = None

	# List of samples ([float])
	voltages = []

	# Iterate over lines
	for samples_file_line in samples_file_lines:

		# Trim string
		samples_file_line = samples_file_line.strip()

		# Skip empty strings
		if not samples_file_line:
			continue

		# Line can be either header line (starting with #) or data line (pure float)
		if samples_file_line[0] == '#':
			samples_file_clock_match = samples_file_clock_regex.match(samples_file_line)
			if samples_file_clock_match:
				clock = float(samples_file_clock_match.group(1))
		else:
			voltage = float(samples_file_line)
			voltages.append(voltage)

	# Check if data was gathered successfuly 
	if clock is None:
		raise Exception('Unknown clock, possibly #CLOCK= header missing')
	if not voltages:
		raise Exception('Missing voltages, no samples found')

	# Output list for PWL lines
	pwl_lines = []

	# Time iterator
	time = 0.0

	# Loop over samples, generate lines
	for voltage in voltages:
		# Single entry consists of time and voltage
		pwl_columns = [format(time, 'f'), repr(voltage)]

		# Join columns using tab
		pwl_line = "\t".join(pwl_columns)

		# Add entry to list
		pwl_lines.append(pwl_line)

		# Move time
		time += clock

	# Join lines to string
	return "\r\n".join(pwl_lines)


#
# Main program
#
if len(sys.argv) <= 1:
	raise Exception("Usage: %s <samples file 1> <samples file 2> <samples file 3> ..." % (sys.argv[0]))

# Extract list of files to process
samples_file_names = sys.argv[1:]

# Iterate over files
for samples_file_name in samples_file_names:
	# Create PWL file name
	pwl_file_name = os.path.splitext(samples_file_name)[0] + '.pwl.txt'

	# Open sample file
	with open(samples_file_name) as samples_file:
		# Read sample file contents
		samples_file_content = samples_file.read()

		# Create PWL file contents
		pwl_file_content = samples_file_content_to_pwl_file_content(samples_file_content)

		# Store PWL file contents
		with open(pwl_file_name, 'w') as pwl_file:
			pwl_file.write(pwl_file_content)
