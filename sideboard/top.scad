$fn = 90;

difference() {
	cube(size = [1422.4000000000, 406.4000000000, 18]);
	translate(v = [0, 388.4000000000, 18]) {
		rotate(a = [-90, 0, 0]) {
			union() {
				translate(v = [-0.3000000000, 0, -0.3000000000]) {
					cube(center = false, size = [142.8400000000, 12.7000000000, 13.0000000000]);
				}
				hull() {
					translate(v = [139.3650000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [140.7581470319, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				hull() {
					translate(v = [287.3550000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [285.9618529681, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				translate(v = [284.1800000000, 0, -0.3000000000]) {
					cube(center = false, size = [142.8400000000, 12.7000000000, 13.0000000000]);
				}
				hull() {
					translate(v = [423.8450000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [425.2381470319, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				hull() {
					translate(v = [571.8350000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [570.4418529681, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				translate(v = [568.6600000000, 0, -0.3000000000]) {
					cube(center = false, size = [142.8400000000, 12.7000000000, 13.0000000000]);
				}
				hull() {
					translate(v = [708.3250000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [709.7181470319, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				hull() {
					translate(v = [856.3150000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [854.9218529681, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				translate(v = [853.1400000000, 0, -0.3000000000]) {
					cube(center = false, size = [142.8400000000, 12.7000000000, 13.0000000000]);
				}
				hull() {
					translate(v = [992.8050000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [994.1981470319, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				hull() {
					translate(v = [1140.7950000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [1139.4018529681, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
				translate(v = [1137.6200000000, 0, -0.3000000000]) {
					cube(center = false, size = [142.8400000000, 12.7000000000, 13.0000000000]);
				}
				hull() {
					translate(v = [1277.2850000000, 0, 2.8750000000]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
					translate(v = [1278.6781470319, 0, 1.4818529681]) {
						rotate(a = [-90, 0, 0]) {
							cylinder(center = false, h = 12.7000000000, r = 3.1750000000);
						}
					}
				}
			}
		}
	}
	translate(v = [0, 401.1000000000, 5.3000000000]) {
		cube(size = [1422.4000000000, 5.3000000000, 12.7000000000]);
	}
}
/***********************************************
*********      SolidPython code:      **********
************************************************
 
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
 
 
************************************************/
