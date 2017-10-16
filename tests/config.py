# coding: utf-8
from os.path import abspath
from os.path import dirname
from os.path import normpath
from site import addsitedir
from sys import path


path.append(normpath(dirname(abspath(__file__)) + "/../src"))
addsitedir("../src/lib")
