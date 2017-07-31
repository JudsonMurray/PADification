# !/usr/bin/env Python3

#   Name:   WILLIMAM GALE
#   Date:   July 30TH 2017
#   Purpose: Relative Resource paths for padification

import os
import sys
import ctypes
import inspect

windll_user32 = ctypes.windll.user32

SCREENWIDTH = windll_user32.GetSystemMetrics(0)

SCREENHEIGHT = windll_user32.GetSystemMetrics(1)

_currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

LOGPATH = (os.path.dirname(os.path.dirname(_currentdir)) + r"\log" )

RESOURCE = (os.path.dirname(os.path.dirname(_currentdir)) + r"\Resource" )

FONT = RESOURCE + r"\PAD\Font"

IMAGE = RESOURCE + r"\PAD\Images"

ATTRIBUTES = IMAGE + r"\Attributes"

AWOKENSKILLS = IMAGE + r"\Awoken Skills"

BADGE = IMAGE + r"\Badges"

LATENTAWOKENSKILLS = IMAGE + r"\LatentAwokenSkills"

PORTRAITS = IMAGE + r"\portraits"

THUMBNAILS = IMAGE + r"\thumbnails"

TYPES = IMAGE + r"\Types"

UI = (os.path.dirname(os.path.dirname(_currentdir)) + r"\src\ui" )
