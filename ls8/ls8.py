#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()

file = sys.argv[1]

cpu.load(file)

cpu.run(mult.ls8)
