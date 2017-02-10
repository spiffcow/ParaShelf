#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 90

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

def squareTabCut(height,width,depth,cutDiameter,count,alternate=False, allAround=False):
    d = []
    tabWidth = width/(count)
    cutOffset = sqrt(cutDiameter/2)/2

    for i in range(0,count):
        if (alternate):
            isSquare = i % 2 != 0
        else:
            isSquare = i % 2 == 0
        if (i > 0 and i < count) or (i == 0 and allAround and isSquare) or (i == count and allAround and not isSquare):
            cutOffsetSign = 1 if isSquare else -1
            d += [
                translate([(i*tabWidth),0,cutDiameter/2])(
                #translate([(i*tabWidth+cutOffsetSign*cutOffset),0,cutOffset])(
                    rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
                )
            ]
            if (allAround):
                d += [
                    translate([(i*tabWidth),0,height-cutDiameter/2])(
                    #translate([(i*tabWidth+cutOffsetSign*cutOffset),0,height-cutOffset])(
                        rotate([-90,0,0])(cylinder(cutDiameter/2,depth, center=False))
                    )
                ]
        if (i < count and isSquare):
            d += [
                translate([(i*tabWidth),0,0])(
                    cube([tabWidth,depth,height],center=False)
                )
            ]

    return union()(*d)

class CutPiece:
    def __init__(self, translation, rotation, geo):
        self.translation = translation
        self.rotation = rotation
        self.geo = geo

    def clone(self):
        return CutPiece(list(self.translation),list(self.rotation),geo.clone())

    def inPlace(self):
        return translate(self.translation)(rotate(self.rotation)(self.geo))


def assembly(shelfHeight, shelfWidth, shelfDepth, kickplateHeight, shelfCount, tabHeight, ply, cutterDiameter, wTabCount, hTabCount, dTabCount, explode):
    rightSide_Top_Cut = CutPiece(
        translation = [0,ply-tabHeight,shelfHeight-ply],
        rotation = [0,0,0],
        geo = squareTabCut(tabHeight, shelfDepth, tabHeight, cutterDiameter, dTabCount,alternate=True,allAround=False)
    )
    leftSide_Top_Cut = CutPiece(
        translation = [0,shelfWidth-ply+tabHeight,shelfHeight-ply],
        rotation = [0,0,0],
        geo = mirror([0,1,0])(rightSide_Top_Cut.geo)
    )
    rightSide_Back_Cut = CutPiece(
        translation = [shelfDepth-ply,ply,0],
        rotation = [0,0,0],
        geo = rotate([180,-90,0])(squareTabCut(tabHeight, shelfHeight-ply+tabHeight, tabHeight, cutterDiameter, hTabCount,alternate=False,allAround=False))
    )
    leftSide_Back_Cut = CutPiece(
        translation = [shelfDepth-ply,shelfWidth-ply+tabHeight,0],
        rotation = [0,0,0],
        geo = rightSide_Back_Cut.geo
    )
    back_rightSide_Cut = CutPiece(
        translation = [shelfDepth-ply+tabHeight,ply,0],
        rotation = [0,0,0],
        geo = rotate([90,-90,0])(squareTabCut(tabHeight, shelfHeight-ply+tabHeight, tabHeight, cutterDiameter, hTabCount,alternate=True,allAround=False))
    )
    back_leftSide_Cut = CutPiece(
        translation = [shelfDepth-ply+tabHeight,shelfWidth-ply,0],
        rotation = [0,0,0],
        geo = mirror([0,1,0])(back_rightSide_Cut.geo)
    )
    back_top_Cut = CutPiece(
        translation = [shelfDepth-ply,shelfWidth+tabHeight,shelfHeight-ply],
        rotation = [0,0,-90],
        geo = squareTabCut(tabHeight, shelfWidth, tabHeight, cutterDiameter, wTabCount,alternate=True,allAround=False)
    )
    top_rightSide_Cut = CutPiece(
        translation = [0,ply,shelfHeight-ply],
        rotation = [90,0,0],
        geo = squareTabCut(tabHeight, shelfDepth, tabHeight, cutterDiameter, dTabCount,alternate=False,allAround=False)
    )
    top_leftSide_Cut = CutPiece(
        translation = [0,shelfWidth-ply,shelfHeight-ply],
        rotation = [-90,0,0],
        geo = mirror([0,1,0])(top_rightSide_Cut.geo)
    )
    top_back_Cut = CutPiece(
        translation = [shelfDepth-ply,shelfWidth,shelfHeight-ply+tabHeight],
        rotation = [-90,0,-90],
        geo = squareTabCut(tabHeight, shelfWidth, tabHeight, cutterDiameter, wTabCount,alternate=False,allAround=False)
    )
    rightSide = CutPiece(
        translation = [0,0,0],
        rotation = [0,0,0],
        geo = union()(
            cube([shelfDepth,ply-tabHeight,shelfHeight-ply+tabHeight]),
            translate([0,ply-tabHeight,0])(cube([shelfDepth-ply+tabHeight,tabHeight,shelfHeight-ply+tabHeight]))
        )
    )
    leftSide = CutPiece(
        translation = [0,shelfWidth-ply,0],
        rotation = [0,0,0],
        geo = union()(
            cube([shelfDepth-ply+tabHeight,tabHeight,shelfHeight-ply+tabHeight]),
            translate([0,tabHeight,0])(cube([shelfDepth,ply-tabHeight,shelfHeight-ply+tabHeight]))
        )
    )
    top = CutPiece(
        translation = [0,0,shelfHeight-ply],
        rotation = [0,0,0],
        geo = union()(
            translate([0,ply-tabHeight,0])(cube([shelfDepth-ply+tabHeight,shelfWidth - 2*(ply-tabHeight), tabHeight])),
            translate([0,0,tabHeight])(cube([shelfDepth,shelfWidth, ply-tabHeight]))
        )
    )
    kickplate = CutPiece(
        translation = [0,0,0],
        rotation = [0,0,0],
        geo = union()(
            translate([0,ply,0])(cube([ply,shelfWidth - 2*ply,kickplateHeight-ply])),
            translate([ply/2,ply/2,0])(cube([ply/2,shelfWidth - ply,kickplateHeight-ply/2]))
        )
    )
    backSide = CutPiece(
        translation = [shelfDepth - ply, ply-tabHeight, 0],
        rotation = [0,0,0],
        geo = union()(
            translate([0,0,0])(cube([ply, shelfWidth - 2 * (ply-tabHeight), shelfHeight-ply+tabHeight]))
        )
    )
    shelfPieces = []
    shelfCutouts = []
    shelfStartHeight = kickplateHeight - ply
    shelfSpacing = (shelfHeight - ply - shelfStartHeight) / (shelfCount)
    shelfCutoutTemplate = squareTabCut(tabHeight, shelfDepth-ply+tabHeight, ply, cutterDiameter, dTabCount,alternate=False,allAround=False)
    shelfBackCutoutTemplate = squareTabCut(tabHeight, shelfWidth-2*tabHeight, ply, cutterDiameter, wTabCount,alternate=False,allAround=False)
    shelfTemplate = difference()(
        translate([0,ply-tabHeight,0])(cube([shelfDepth-ply+tabHeight,shelfWidth-2*(ply-tabHeight), ply])),
        translate([0,ply,0])(rotate([90,0,0])(shelfCutoutTemplate)),
        translate([0,shelfWidth-ply,0])(rotate([-90,0,0])(mirror([0,1,0])(shelfCutoutTemplate))),
        translate([shelfDepth-ply, ply, 0])(rotate([90,0,90])(shelfBackCutoutTemplate))
    )

    shelfSideCutoutTemplate = squareTabCut(ply, shelfDepth, tabHeight, cutterDiameter, dTabCount,alternate=True,allAround=True)
    shelfCutoutTemplateForBack = squareTabCut(ply, shelfWidth-2*tabHeight, tabHeight, cutterDiameter, wTabCount,alternate=True,allAround=True)
    for i in range(0,shelfCount):
        shelfPieces += [CutPiece(
            translation = [0,0,shelfStartHeight+i*shelfSpacing],
            rotation = [0,0,0],
            geo = shelfTemplate
        )]
        shelfCutouts += [
            CutPiece(
                translation = [0,ply-tabHeight,shelfStartHeight+i*shelfSpacing],
                rotation = [0,0,0],
                geo = shelfSideCutoutTemplate
            ),
            CutPiece(
                translation = [0,shelfWidth-ply+tabHeight,shelfStartHeight+i*shelfSpacing],
                rotation = [0,0,0],
                geo = mirror([0,1,0])(shelfSideCutoutTemplate)
            ),
            CutPiece(
                translation = [shelfDepth-ply+tabHeight, ply, shelfStartHeight+i*shelfSpacing],
                rotation = [0,0,90],
                geo = shelfCutoutTemplateForBack
            )
        ]
    renderedCutouts = union()(*[s.inPlace() for s in shelfCutouts])

    rightSideRendered = rightSide.inPlace() - rightSide_Top_Cut.inPlace() - renderedCutouts - kickplate.inPlace() - rightSide_Back_Cut.inPlace()
    leftSideRendered = leftSide.inPlace() - leftSide_Top_Cut.inPlace() - renderedCutouts - kickplate.inPlace() - leftSide_Back_Cut.inPlace()
    backRendered = backSide.inPlace() - renderedCutouts - back_rightSide_Cut.inPlace() - back_leftSide_Cut.inPlace() - back_top_Cut.inPlace()
    topRendered = top.inPlace() - top_rightSide_Cut.inPlace() - top_leftSide_Cut.inPlace() - top_back_Cut.inPlace()
    shelves = [s.inPlace() - kickplate.inPlace() for s in shelfPieces]

    scad_render_to_file(rightSideRendered, "rightside.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    scad_render_to_file(leftSideRendered, "leftside.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    scad_render_to_file(backRendered, "back.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    scad_render_to_file(topRendered, "top.scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
    for i in range(0,len(shelves)):
        scad_render_to_file(shelves[i], "shelf" + str(i) + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)

    return union()(
        color("red")(back_leftSide_Cut.inPlace()),
        #union()(*shelves),
        #back(explode)(color("red")(rightSideRendered)),
        #forward(explode)(color("red")(leftSideRendered)),
        #color("blue")( topTabCut.inPlace()),
        #color("blue")( top_leftSide_Cut.inPlace()),
        #up(explode)(color("blue")(topRendered)),
        #down(explode)(color("blue")(kickplate.inPlace())),
        right(explode)(color("green")(backRendered)),
        #color("green")(leftPanel)
        #color("red")(leftSide_Top_Cut.inPlace())
    )
    #top -= rightPanel
    #top -= leftPanel
    #intersection()(top,offset(0.001)(top))

if __name__ == '__main__':
    uom = 25.4
    ply = 17.6#11.7#23/32 * uom
    a = assembly(
        shelfHeight = 30 * uom,
        shelfWidth = 37 * uom,
        shelfDepth = 18 * uom,
        kickplateHeight = 3 * uom,
        shelfCount = 2,
        tabHeight = 2/3 * ply,
        ply = ply,
        cutterDiameter = 4,
        wTabCount = 9,
        hTabCount = 9,
        dTabCount = 5,
        explode = 50
    )
    scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)
