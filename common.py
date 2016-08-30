#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
# File: common.py
# Author: Sibo Jia <sibojia.cs@gmail.com>
import os, sys

def script_path():
    path = os.path.realpath(sys.argv[0])
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return os.path.abspath(path)
