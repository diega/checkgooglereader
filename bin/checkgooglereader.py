#!/usr/bin/env python

import logging.config
logging.config.fileConfig('bin/logging.conf')


import sys
from os.path import dirname, join, pardir
sys.path.insert(0, join(dirname(__file__), pardir, 'share',
                        'checkgooglereader', 'lib'))
from checkgooglereader import main

main()

