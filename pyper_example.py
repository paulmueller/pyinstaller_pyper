#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A Python script that uses numpy and pyper.
"""
from __future__ import division, print_function

import numpy as np
import pyper

xs = np.linspace(0,1,10)

#Open a pyper instance
r1 = pyper.R(use_pandas = True) 
r1.assign("xs", xs) 
r1("DFRAME=data.frame(xs)")
r1("result <- DFRAME[xs]*2")   
result = r1.get("result")
data = result.as_matrix().reshape(-1)

assert np.allclose(2*xs, data), "pyper does not work"

print("Everything OK: numpy and pyper working.")

if hasattr(sys, "frozen"):
    print("Freezing of this script succeeded!")
