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


def get_R_binary(verbose=False):
    # additional search paths
    Rpaths = list()

    # win
    Rroot_win = "C:\\Program Files\\R"
    append_folders = ["", "\\bin\\i386"]
    if os.path.exists(Rroot_win):
        for append in append_folders:
            # This will work independent of the installed R version
            Rpaths += [ os.path.join(Rroot_win, d+append) for d in os.listdir(Rroot_win) ]
    # win frozen
    if hasattr(sys, "frozen"):
        Rroot_win_frozen = os.path.join(os.path.abspath(sys._MEIPASS), "R")
        if os.path.exists(Rroot_win_frozen):
            for append in append_folders:
                Rpaths += [  os.path.join(Rroot_win_frozen, d+append) for d in os.listdir(Rroot_win_frozen) ]

    # linux
    Rpaths += ["/usr/bin"]

    Rexes = list()
    for binary in ["R", "R.exe"]:
        Rexes += [ os.path.join(loc, binary) for loc in Rpaths ]

    Rexe_avail = [ r for r in Rexes if os.path.exists(r) ]

    if verbose:
        print("Available binaries:", Rexe_avail)

    # standard path search:
    if len(Rexe_avail) == 0:
        Rexe = "R"
    else:
        Rexe = Rexe_avail[0]

    # find other installation:

    if verbose: 
        print("Using R: ", Rexe)
    
    return Rexe


if __name__ == "__main__":
    Rexe = get_R_binary(verbose=True)
    #Open a pyper instance
    r1 = pyper.R(use_pandas=True, RCMD=Rexe) 
    # Perform a simple computation
    xs = np.linspace(0,1,10)
    r1.assign("xs", xs) 
    r1("DFRAME=data.frame(xs)")
    r1("result <- DFRAME[xs]*2")   
    # Retrieve the result
    result = r1.get("result")
    import IPython
    IPython.embed()
    try:
        # R 3.0.4 linux
        data = result.as_matrix().reshape(-1)
    except AttributeError:
        # `result` is already an ndarray?
        # R 3.2.2 windows
        data = np.array(result, dtype=float).reshape(-1)

    # Validate the result
    assert np.allclose(2*xs, data), "pyper does not work"

    print("Everything OK: numpy and pyper are working.")

    if hasattr(sys, "frozen"):
        print("Freezing of this script succeeded!")
