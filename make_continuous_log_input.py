#!/usr/bin/python -u
#############################################################################
# 
# This is a simple little script to generate output on both stdout 
# as well as stderr, to test that your redirection for logging is 
# setup correctly.
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

import sys
import time

count = 1

while True:
    print "Creating Log data on stdout", count
    print >> sys.stderr, "Creating Log data on stderr", count
    count = count + 1
    if count % 10 == 0:
        time.sleep(2)
    else:
        time.sleep(0.1)


