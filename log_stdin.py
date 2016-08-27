#!/usr/bin/python
#############################################################################
# 
# This script allows you to capture stdin from a program and log it 
# in an intelligent, configurable manner.
#
# MIT License
# 
# Copyright (c) 2016, Michael Becker (michael.f.becker@gmail.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS 
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF 
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY 
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT 
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 
#############################################################################
"""
This script allows you to capture stdin from a program and log it 
in an intelligent, configurable manner.
"""
import sys
import os
import shutil
import json
import argparse
import signal
import datetime


def build_log_filenames(basename, path, max_number):
    """Create all of the logfile names."""
    filenames = []
    name = os.path.join(path, basename)
    filenames.append(name)
    for i in range(1, max_number):
        filenames.append(name + "." + str(i))
    return filenames


def rotate_logs(filenames):
    """Rotate all of the logfiles, dropping the last one."""
    max_number = len(filenames)
    # Remove the oldest one if it exists.
    if os.path.isfile(filenames[max_number - 1]):
        os.remove(filenames[max_number - 1])
    # And rename all of the other ones down if they exist.
    for i in range(max_number - 2, -1, -1):
        if os.path.isfile(filenames[i]):
            shutil.move(filenames[i], filenames[i+1])


def is_max_size(filename, max_size):
    """Check if a file is at the max allowable size."""
    # If the file isn't there, it's not at the max size.
    if not os.path.isfile(filename):
        return False
    statinfo = os.stat(filename)
    if statinfo.st_size > max_size:
        return True
    else:
        return False


def log_stdin(filenames, max_size, timestamp):
    """Runs forever, writing stdin to log files"""

    if is_max_size(filenames[0], max_size):
        rotate_logs(filenames)

    # We want to exit cleanly if someone hits CTRL-C.
    def ctrl_c_handler(signum, frame):
        """Clean exit"""
        print "Exiting log_stdin on CTRL-C"
        log.close()
        sys.exit()

    signal.signal(signal.SIGINT, ctrl_c_handler)

    log = open(filenames[0], "a", 1) # line buffer
    while True:
        line = sys.stdin.readline()
        if line == '':
            break

        # If we are timestamping the input, append it.
        if timestamp:
            ts = datetime.datetime.now()
            line = "[" + str(ts) + "] " + line

        log.write(line)
        if is_max_size(filenames[0], max_size):
            log.close()
            rotate_logs(filenames)
            log = open(filenames[0], "a", 1)  # line buffer

    # If we ever do fall out, make sure we close so the final 
    # data is written to file.
    log.close()


def load_config_file(filename):
    """Read in the JSON config file."""
    try:
        f = open(filename, 'r')
        config = json.load(f)
        f.close()
        return config

    except ValueError:
        print "Config file", filename, "contains an error."

    except IOError as e:
        print "Config file", filename, "cannot be opened,", e.strerror


def set_config_default():
    """
    Set the configuration defaults, keeping the code in 
    one location.
    """
    config = {  "logfile_name": "logfile.dat",
                "path": ".",
                "max_number_logfiles": 5,
                "max_logfile_size": 1000000,
                "timestamp": False
            }
    return config


def create_default_config(filename):
    """Create a default JSON config file."""
    config = set_config_default()
    f = open(filename, "w")
    json.dump(config, f)
    f.close()
    print "Default config file", filename, "created."
    sys.exit()


# Main script starts here
parser = argparse.ArgumentParser(
    description="Allows you to capture stdin from a program " 
    + "and log it in an intelligent, configurable manner. "
    + "Command line args override confile file settings.")
parser.add_argument("-c", "--config-file", help="specify a JSON config file")
parser.add_argument("-f", "--logfile-name", help="base logfile name.")
parser.add_argument("-p", "--path", help="log file directory")
parser.add_argument("-m", "--max-logfile-size", help="max file size in bytes")
parser.add_argument("-n", "--max-number-logfiles", help="total number of logfiles retained")
parser.add_argument("-t", "--timestamp", action='store_true', help="add a timestamp to every entry")
parser.add_argument("--no-timestamp", action='store_true', help="do not add timestamps")
parser.add_argument("--create-config-file", help="generate a config JSON file with script defaults")
args = parser.parse_args()


if args.create_config_file:
    create_default_config(args.create_config_file)

# Start with the config file if we have it.
if args.config_file:
    config = load_config_file(args.config_file)
    if not config:
        # For a bad parse, set defaults.
        config = set_config_default()
else:
    # No config file, start with defaults.
    config = set_config_default()

# Always allow command line args to override the config file.
if args.logfile_name:
    config["logfile_name"] = args.logfile_name

if args.path:
    config["path"] = args.path

if args.max_number_logfiles:
    config["max_number_logfiles"] = int(args.max_number_logfiles)

if args.max_logfile_size:
    config["max_logfile_size"] = int(args.max_logfile_size)

if args.timestamp:
    config["timestamp"] = True

if args.no_timestamp:
    config["timestamp"] = False

# Build the logfile names all at once.
filenames = build_log_filenames(config["logfile_name"], 
                                config["path"], 
                                config["max_number_logfiles"])

# And start logging forever.
log_stdin(filenames, config["max_logfile_size"], config["timestamp"])


