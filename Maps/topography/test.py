#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PIL import Image
from math import *
from pyproj import Proj
from time import time

from ConfigParser import SafeConfigParser
params=SafeConfigParser()
params.read('../../param.ini')


print params.get('Source_Image','src_img')
print params.get('Maps_Size','radius_of_the_globe')
