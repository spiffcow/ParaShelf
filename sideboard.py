#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *
from tabs import *
from CutPiece import *

SEGMENTS = 90




def assembly(totalLength, sectionLength, cabinetHeight, cabinetWidth, legBoxHeight, legHeight, legAngle, ply, lTabCount, wTabCount, cutterDiameter, tabDepth, explode):
	top = CutPiece(
		translation = [0,0,cabinetHeight-ply],
		rotation = [0,0,0],
		geo = difference()(
			cube([totalLength, cabinetWidth, ply]),
			
			#back panel tabs
			translate([0,cabinetWidth-ply, ply])(
				rotate([-90,0,0])(squareTabCut(tabDepth, totalLength, tabDepth, cutterDiameter, lTabCount,alternate=False,allAround=False,hideHoles=False))
			),
			translate([0,cabinetWidth-ply+tabDepth, ply-tabDepth])(
				cube([totalLength, ply-tabDepth, tabDepth])
			)
		)
	)
	bottom = CutPiece(
		translation = [0,0,0],
		rotation = [0,0,0],
		geo = cube([totalLength, cabinetWidth, ply])
	)
	
	lSideOuter = CutPiece(
		translation = [0,0,ply],
		rotation = [0,0,0],
		geo = cube([ply, cabinetWidth, cabinetHeight-2*ply])
	)
	
	rSideOuter = CutPiece(
		translation = [totalLength-ply,0,ply],
		rotation = [0,0,0],
		geo = cube([ply, cabinetWidth, cabinetHeight-2*ply])
	)
	scad_render_to_file(top.geo, "sideboard\\top.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

	#scad_render_to_file(combined, "bench\\combined.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

if __name__ == '__main__':
	uom = 25.4
	ply = 18
	assembly(
		totalLength = 56 * uom,
		sectionLength = 20 * uom,
		cabinetHeight = 12 * uom,
		cabinetWidth = 16 * uom,
		legBoxHeight=2 * uom,
		legHeight = 6 * uom,
		legAngle = 30,
		ply = ply,
		lTabCount = 10,
		wTabCount = 5,
		cutterDiameter = 1/4*uom,
		tabDepth = 0.5 * uom,
		explode = 50
	)
