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




def assembly(sectionLength, lSections, wSections, height, ply, sectionTabCount, cutterDiameter, openingOffset, topAndBottomSegments, maxLengthSectionCount, explode):
    length = ply + lSections * (ply + sectionLength)
    width = ply + wSections * (ply + sectionLength)
    tabHeight = ply

    top = CutPiece(
        translation = [0,0,height-ply],
        rotation = [0,0,0],
        geo = cube([width, length, ply])
    )
    bottom = CutPiece(
        translation = [0,0,0],
        rotation = [0,0,0],
        geo = cube([width, length, ply])
    )

    lSide = CutPiece(
        translation = [0,0,0],
        rotation = [0,0,0],
        geo = cube([ply, length, height])
    )
    lSides = [lSide]
    for i in range(1,wSections+1):
        newLSide = CutPiece(
            translation = [i * (ply + sectionLength), 0, 0],
            rotation = [0,0,0],
            geo = lSide.geo
        )
        lSides += [newLSide]

    wSide = CutPiece(
        translation = [0,0,0],
        rotation = [0,0,0],
        geo = cube([width, ply, height])
    )
    wSides = [wSide]
    for i in range(1,lSections+1):
        newWSide = CutPiece(
            translation = [0, i * (ply + sectionLength), 0],
            rotation = [0,0,0],
            geo = wSide.geo
        )
        wSides += [newWSide]

    wSideCutouts = []
    radius = (height - 2 * openingOffset) / 2
    for i in range(0,wSections):
        wSideCutouts += [
        CutPiece(
            translation = [ply + i * (ply + sectionLength), 0, 0],
            rotation = [0,0,0],
            geo = union()(
                translate([openingOffset+radius, 0, height/2])(
                    rotate([-90,0,0])(
                        cylinder(radius,length)
                    )
                ),
                translate([sectionLength-(openingOffset+radius), 0, height/2])(
                    rotate([-90,0,0])(
                        cylinder(radius,length)
                    )
                ),
                translate([openingOffset+radius, 0, openingOffset])(
                    cube([sectionLength-2*(openingOffset+radius), length, height - 2*openingOffset])
                )
            )
        )
    ]

    for i in range(0,wSections+1):
        wSideCutouts += [
            CutPiece(
                translation = [i * (ply + sectionLength), 0, 0],
                rotation = [0,0,0],
                geo = union()(
                    cube([ply, length, height/2]),
                    translate([0, 0, height/2-cutterDiameter/2])(
                        rotate([-90,0,0])(
                            cylinder(cutterDiameter/2,length)
                        )
                    ),
                    translate([ply, 0, height/2-cutterDiameter/2])(
                        rotate([-90,0,0])(
                            cylinder(cutterDiameter/2,length)
                        )
                    ),
                )
            ),
            CutPiece(
                translation = [i * (ply + sectionLength), 0, 0],
                rotation = [0,0,0],
                geo = union()(
                    cube([ply, length, height/2]),
                    translate([0, 0, height/2-cutterDiameter/2])(
                        rotate([-90,0,0])(
                            cylinder(cutterDiameter/2,length)
                        )
                    ),
                    translate([ply, 0, height/2-cutterDiameter/2])(
                        rotate([-90,0,0])(
                            cylinder(cutterDiameter/2,length)
                        )
                    ),
                )
            )
        ]

    lSideCutouts = []
    for i in range(0,lSections+1):
        lSideCutouts += [
            CutPiece(
                translation = [0, ply + i * (ply + sectionLength), 0],
                rotation = [0,0,0],
                geo = union()(
                    translate([0, openingOffset+radius, height/2])(
                        rotate([0,90,0])(
                            cylinder(radius,width)
                        )
                    ),
                    translate([0, sectionLength-(openingOffset+radius), height/2])(
                        rotate([0,90,0])(
                            cylinder(radius,width)
                        )
                    ),
                    translate([0, openingOffset+radius, openingOffset])(
                        cube([width, sectionLength-2*(openingOffset+radius), height - 2*openingOffset])
                    )
                )
            ),
            CutPiece(
                translation = [0, i * (ply + sectionLength), 0],
                rotation = [0,0,0],
                geo = union()(
                    translate([0,0,height/2])(cube([width, ply, height/2])),
                    translate([0, 0, height/2+cutterDiameter/2])(
                        rotate([0,90,0])(
                            cylinder(cutterDiameter/2,width)
                        )
                    ),
                    translate([0, ply, height/2+cutterDiameter/2])(
                        rotate([0,90,0])(
                            cylinder(cutterDiameter/2,width)
                        )
                    ),
                )
            )
        ]


    tabCutoutTemplate = squareTabCut(ply, sectionLength + 2*ply, ply, cutterDiameter, sectionTabCount,alternate=False,allAround=False,hideHoles=False)
    tabAltCutoutTemplate = squareTabCut(ply, sectionLength + 2*ply, ply, cutterDiameter, sectionTabCount,alternate=True,allAround=True,hideHoles=False)
    tabAltCutoutEndTemplate = squareTabCut(ply, sectionLength + 2*ply, ply, cutterDiameter, sectionTabCount,alternate=True,allAround=False,hideHoles=False)
    lTabCutouts = []
    wTabCutouts = []
    surfaceTabCutouts = []
    for i in range(0,wSections+1):
        for j in range(0,lSections+1):
            lTabCutouts += [
                CutPiece(
                    translation = [ply + i * (ply + sectionLength), j * (ply + sectionLength), height-ply],
                    rotation = [0,0,90],
                    geo = tabCutoutTemplate
                )
            ]
            lTabCutouts += [
                CutPiece(
                    translation = [i * (ply + sectionLength), j * (ply + sectionLength), ply],
                    rotation = [180,0,90],
                    geo = tabCutoutTemplate
                )
            ]
            wTabCutouts += [
                CutPiece(
                    translation = [j * (ply + sectionLength),  i * (ply + sectionLength), height-ply],
                    rotation = [0,0,0],
                    geo = tabCutoutTemplate
                )
            ]
            wTabCutouts += [
                CutPiece(
                    translation = [j * (ply + sectionLength), ply + i * (ply + sectionLength), ply],
                    rotation = [180,0,0],
                    geo = tabCutoutTemplate
                )
            ]

            if i == 0:
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [ply + i * (ply + sectionLength), j * (ply + sectionLength), height],
                        rotation = [-90,0,90],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [ply + i * (ply + sectionLength), j * (ply + sectionLength), ply],
                        rotation = [-90,0,90],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
            elif i == wSections:
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), ply + j * (ply + sectionLength), height-ply],
                        rotation = [90,0,90],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), ply + j * (ply + sectionLength), 0],
                        rotation = [90,0,90],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
            else:
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), j * (ply + sectionLength), height-ply],
                        rotation = [90,0,90],
                        geo = tabAltCutoutTemplate
                    )
                ]
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), j * (ply + sectionLength), 0],
                        rotation = [90,0,90],
                        geo = tabAltCutoutTemplate
                    )
                ]

            if j == 0:
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), ply + j * (ply + sectionLength), height-ply],
                        rotation = [90,0,0],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), ply + j * (ply + sectionLength), 0],
                        rotation = [90,0,0],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
            elif j == lSections:
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), j * (ply + sectionLength), height],
                        rotation = [-90,0,0],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), j * (ply + sectionLength), ply],
                        rotation = [-90,0,0],
                        geo = tabAltCutoutEndTemplate
                    )
                ]
            else:
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), j * (ply + sectionLength), height],
                        rotation = [-90,0,0],
                        geo = tabAltCutoutTemplate
                    )
                ]
                surfaceTabCutouts += [
                    CutPiece(
                        translation = [i * (ply + sectionLength), j * (ply + sectionLength),  ply],
                        rotation = [-90,0,0],
                        geo = tabAltCutoutTemplate
                    )
                ]


    wSideCutoutsRendered = [s.inPlace() for s in wSideCutouts]
    lSideCutoutsRendered = [s.inPlace() for s in lSideCutouts]
    lTabCutoutsRendered =  [s.inPlace() for s in lTabCutouts]
    wTabCutoutsRendered =  [s.inPlace() for s in wTabCutouts]
    surfaceTabCutoutsRendered =  [s.inPlace() for s in surfaceTabCutouts]
    lSidesRendered = difference()(union()(*[s.inPlace() for s in lSides]), lSideCutoutsRendered, lTabCutoutsRendered)
    wSidesRendered = difference()(union()(*[s.inPlace() for s in wSides]), wSideCutoutsRendered, wTabCutoutsRendered)
    topRendered = difference()(top.inPlace(), surfaceTabCutoutsRendered)
    bottomRendered = difference()(bottom.inPlace(), surfaceTabCutoutsRendered)
    combined = union()(
        up(explode)(color("blue")(topRendered)),
        down(explode)(color("blue")(bottomRendered)),
        down(explode/2)(color("yellow")(lSidesRendered)),
        up(explode/2)(color("red")(wSidesRendered)),
    )
    if topAndBottomSegments == 1:
        scad_render_to_file(top.reverse()(topRendered), "bench\\top.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
        scad_render_to_file(bottom.reverse()(bottomRendered), "bench\\bottom.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    else:
        for i in range(0,topAndBottomSegments):
            blinders = [translate([0,j*length/topAndBottomSegments,0])(cube([width,length/topAndBottomSegments,ply])) for j in range(0,topAndBottomSegments) if j != i]
            topSegment = difference()(
                top.reverse()(topRendered),
                union()(*blinders)
            )
            scad_render_to_file(topSegment, "bench\\top" + str(i) + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
            bottomSegment = difference()(
                bottom.reverse()(bottomRendered),
                union()(*blinders)
            )
            scad_render_to_file(bottomSegment, "bench\\bottom" + str(i) + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)


    for i in range(0,len(lSides)):
        rendered = lSides[i].reverse()(
            difference()(
                lSides[i].inPlace(),
                lSideCutoutsRendered,
                lTabCutoutsRendered
            )
        )
        if maxLengthSectionCount == lSections:
            scad_render_to_file(rendered, "bench\\lside" + str(i) + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
        else:
            j = i % int(lSections/maxLengthSectionCount)
            while j < lSections:
                blinders = union()(*[translate([0,k*(sectionLength+ply),0])(cube([ply,sectionLength+ply,height])) for k in range(0,lSections) if k < j or k >= (j+maxLengthSectionCount)])
                scad_render_to_file(difference()(rendered, blinders), "bench\\lside" + str(i) + "_" + str(int(j/maxLengthSectionCount)) + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
                j += maxLengthSectionCount

    for i in range(0,len(wSides)):
        rendered = wSides[i].reverse()(
            difference()(
                wSides[i].inPlace(),
                wSideCutoutsRendered,
                wTabCutoutsRendered
            )
        )
        scad_render_to_file(rendered, "bench\\wside" + str(i) + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

    scad_render_to_file(combined, "bench\\combined.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

if __name__ == '__main__':
    uom = 25.4
    ply = 12#7/16 * uom
    assembly(
        sectionLength = 11 * uom,
        lSections = 2,
        wSections = 2,
        height = 6 * uom,
        ply = ply,
        sectionTabCount = 5,
        cutterDiameter = 4,
        openingOffset = 1 * uom,
        topAndBottomSegments = 1,
        maxLengthSectionCount = 2,
        explode = 15
    )
