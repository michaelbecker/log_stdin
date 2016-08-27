# log_stdin #

This is a python 2.7 script to capture everything from stdin and log it intelligently 
to a set of rotating log files. Why would this be useful? Well, if you are using a 
program that sends output to the terminal and you want or need to log it, this
allows you to do that without re-writing the entire program you are using.

## Brief Examples ##
To capture a program's output, simply use the following:
```
./cout_cerr | ./log_stdin.py --config-file log_stdin_config.json
```
This is assuming that you make the script log_stdin.py executable.

To capture a program's output both from stdout and stderr:
```
./cout_cerr 2>&1 | ./log_stdin.py --config-file log_stdin_config.json
```
_We just use standard shell redirection to get both into the script._

## Usage ##
_For the latest usage, just run ./log_stdin.py --help_

```
usage: log_stdin.py [-h] [-c CONFIG_FILE] [-f LOGFILE_NAME] [-p PATH]
                    [-m MAX_LOGFILE_SIZE] [-n MAX_NUMBER_LOGFILES] [-t]
                    [--no-timestamp] [--create-config-file CREATE_CONFIG_FILE]

Allows you to capture stdin from a program and log it in an intelligent,
configurable manner. Command line args override confile file settings.

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        specify a JSON config file
  -f LOGFILE_NAME, --logfile-name LOGFILE_NAME
                        base logfile name.
  -p PATH, --path PATH  log file directory
  -m MAX_LOGFILE_SIZE, --max-logfile-size MAX_LOGFILE_SIZE
                        max file size in bytes
  -n MAX_NUMBER_LOGFILES, --max-number-logfiles MAX_NUMBER_LOGFILES
                        total number of logfiles retained
  -t, --timestamp       add a timestamp to every entry
  --no-timestamp        do not add timestamps
  --create-config-file CREATE_CONFIG_FILE
                        generate a config JSON file with script defaults
```


## Default Configuration File Options ##
```
{
    "logfile_name": "logfile.dat",  // base logfile name
    "path": ".",                    // log file directory
    "max_number_logfiles": 5,       // total number of logfiles retained
    "max_logfile_size": 1000000,    // max file size in bytes
    "timestamp": false              // do not add timestamps
}
```
_Note that the comments are not valid JSON and are only to explain the option._

