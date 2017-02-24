
#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

class CutPiece:
    def __init__(self, translation, rotation, geo):
        self.translation = translation
        self.rotation = rotation
        self.geo = geo

    def clone(self):
        return CutPiece(list(self.translation),list(self.rotation),geo.clone())

    def inPlace(self):
        return translate(self.translation)(rotate(self.rotation)(self.geo))

    def reverse(self):
        return translate([-x for x in self.translation])(rotate([-x for x in self.rotation]))
