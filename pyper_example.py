#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Python script that uses numpy and pyper.
"""
from __future__ import division, print_function

import os
import numpy as np
import pyper
import sys

xs = np.linspace(0,1,10)


# additional path searches
Rpaths = ["C:\\Program Files\\R\\R-3.2.2\\bin\\i386",
          "C:\\Program Files\\R\\R-3.2.2",
          "/usr/bin/"]

Rexes = list()
for binary in ["R", "R.exe"]:
    Rexes += [ os.path.join(loc, binary) for loc in Rpaths ]

# standard path search:
Rexe = "R"

# find other installation:
for b in Rexes:
    if os.path.exists(b):
        Rexe = b
        break
print("Using R: ", Rexe)


#Open a pyper instance
r1 = pyper.R(use_pandas=True, RCMD=Rexe) 
r1.assign("xs", xs) 
r1("DFRAME=data.frame(xs)")
r1("result <- DFRAME[xs]*2")   
result = r1.get("result")
try:
    # R 3.0.4 linux
    data = result.as_matrix().reshape(-1)
except:
    # R 3.2.2 windows
    data = result.reshape(-1)
        
assert np.allclose(2*xs, data), "pyper does not work"

print("Everything OK: numpy and pyper working.")

if hasattr(sys, "frozen"):
    print("Freezing of this script succeeded!")
