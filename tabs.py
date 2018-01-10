
#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

def tabs(height,width,depth,cutDiameter,count,closeSides=True,dovetail=False):
	singleTab = hull()(
		cube([width/count,depth,height-cutDiameter/2]),
		translate([cutDiameter/2,0,height-cutDiameter/2])(
			rotate([-90,0,0])(cylinder(cutDiameter/2,depth))
		),
		translate([width/count-cutDiameter/2,0,height-cutDiameter/2])(
			rotate([-90,0,0])(cylinder(cutDiameter/2,depth))
		)
	)
	d = left(cutDiameter/2)(
		cube([width-cutDiameter-0.01,depth-0.01,height-cutDiameter-0.01])
	)
	for i in range(count):
		if i % 2 == 0:
			d += left(i*width/count)(singleTab)
		else:
			d -=  up(height)(
				left((i+1)*width/count)(
					rotate([0,180,0])(singleTab)
				)
			)

	if closeSides:
		if (count % 2 == 0):
			d += cube([cutDiameter/2,depth,height])
			d -= left(width-cutDiameter/2)(
				cube([cutDiameter/2,depth,height])
			)
		else:
			d += cube([cutDiameter/2,depth,height])
			d += left(width-cutDiameter/2)(
				cube([cutDiameter/2,depth,height])
			)
	return d

def tabsNoMesh(height,width,depth,cutDiameter,count,closeSides=True,dovetail=False,blindDepth=0):
	singleTab = union()(
		cube([width/count,depth,height-cutDiameter/2]),
		translate([cutDiameter/2,0,0])(
			cube([width/count-cutDiameter,depth,height])
		),
		translate([cutDiameter/2,0,height-cutDiameter/2])(
			rotate([-90,0,0])(cylinder(cutDiameter/2,depth))
		),
		translate([width/count-cutDiameter/2,0,height-cutDiameter/2])(
			rotate([-90,0,0])(cylinder(cutDiameter/2,depth))
		)
	)
	d = cube([width-cutDiameter,depth,height-cutDiameter])
	for i in range(count):
		if i % 2 == 0:
			d += left(i*width/count)(singleTab)
		else:
			d -=  up(height)(
				left((i+1)*width/count)(
					rotate([0,180,0])(singleTab)
				)
			)

	if closeSides:
		if (count % 2 == 0):
			d += cube([cutDiameter/2,depth,height])
			d -= left(width-cutDiameter/2)(
				cube([cutDiameter/2,depth,height])
			)
		else:
			d += cube([cutDiameter/2,depth,height])
			d += left(width-cutDiameter/2)(
				cube([cutDiameter/2,depth,height])
			)

	if blindDepth > 0:
		d += translate([0,depth-blindDepth,0])(
			cube([width,blindDepth,height])
		)
	return d

def dovetailCutout(height,width,depth,cutDiameter,count):
	d = []
	spacing = width/(count-1)
	tabWidth = width/(count+1)
	hyp = sqrt(height*height + (tabWidth/4)*(tabWidth/4))
	cs = height/hyp
	s = (tabWidth/4)/hyp

	for i in range(0,count-1):
			spaceCount = i
			d += [
				hull()(
					translate([spaceCount*spacing,0,0])(
						cube([tabWidth,depth,0.01])
					),
					translate([spaceCount*spacing + 0.25*tabWidth,0,0])(
						cube([tabWidth/2,depth,height])
					)
				),
				translate([spaceCount*spacing + cs*(cutDiameter/2),0,-s*(cutDiameter/2)])(
					rotate([-90,0,0])(cylinder(cutDiameter/2,depth))
				),
				translate([spaceCount*spacing + tabWidth - cs*(cutDiameter/2),0,-s*(cutDiameter/2)])(
					rotate([-90,0,0])(cylinder(cutDiameter/2,depth))
				)
			]
	return left((spacing-tabWidth)/2)(union()(*d))

def squareTabCut(height,width,depth,cutDiameter,count,alternate=False, allAround=False, hideHoles=False, tolerance=0.3):
	d = []
	tabWidth = width/(count)
	cutOffset = sqrt(cutDiameter/2)

	for i in range(0,count+1):
		if (alternate):
			isSquare = i % 2 != 0
		else:
			isSquare = i % 2 == 0
		cutOffsetSign = 1 if isSquare else -1
		if hideHoles:
			d += [
				translate([(i*tabWidth),0,cutDiameter/2])(
					rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
				)
			]
		else:
			d += [
				hull()(
					translate([(i*tabWidth+cutOffsetSign*(cutDiameter/2-tolerance)),0,cutDiameter/2-tolerance])(
						rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
					),
					translate([(i*tabWidth+cutOffsetSign*(cutOffset-tolerance)),0,cutOffset-tolerance])(
						rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
					)
				)
			]
		if (allAround):
			if hideHoles:
				d += [
					translate([(i*tabWidth),0,height-cutDiameter/2-tolerance])(
						rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
					)
				]
			else:
				d += [
					hull()(
						translate([(i*tabWidth+cutOffsetSign*(cutDiameter/2-tolerance)),0,height-cutDiameter/2])(
							rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
						),
						translate([(i*tabWidth+cutOffsetSign*(cutOffset-tolerance)),0,height-cutOffset])(
							rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
						)
					)
				]
		if (i < count and isSquare):
			d += [
				translate([(i*tabWidth)-tolerance,0,-tolerance])(
					cube([tabWidth+2*tolerance,depth,height+tolerance],center=False)
				)
			]

	return union()(*d)
