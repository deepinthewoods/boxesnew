#!/usr/bin/env python3
# Copyright (C) 2013-2014 Florian Festi
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from boxes import *
from boxes.lids import LidSettings
import math

class PedalBox(Boxes):
    """A simple Box"""

    description = "This box is kept simple on purpose. If you need more features have a look at the UniversalBox."
    
    ui_group = "Box"

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.addSettingsArgs(LidSettings)
        self.buildArgParser("x", "y", "h", "outside", "bottom_edge")
        self.argparser.add_argument(
            "--lip_width",
            action="store",
            type=float,
            default=8,
            help="width of lip",
        )
        self.argparser.add_argument(
            "--top_thickness",
            action="store",
            type=float,
            default=3,
            help="thickness of top",
        )
        self.argparser.add_argument(
            "--pillar_width",
            action="store",
            type=float,
            default=20,
            help="width of reinforcing pillars",
        )
        self.argparser.add_argument(
            "--number_of_pillars",
            action="store",
            type=int,
            default=8,
            help="number of reinforcing pillars",
        )
        self.argparser.add_argument(
            "--switch_diameter",
            action="store",
            type=int,
            default=8,
            help="diameter of holes for switches",
        )
        self.argparser.add_argument(
            "--switches_per_side",
            action="store",
            type=int,
            default=8,
            help="number of switches on each side",
        )
        self.argparser.add_argument(
            "--switches_edge_distance",
            action="store",
            type=int,
            default=20,
            help="distance of switch centre from edge",
        )
    
    def xHoles(self):
        self.fingerHolesAt(self.thickness/2.0 + self.top_thickness, 0, self.x)

    def yHoles(self):
        self.fingerHolesAt(self.thickness/2.0 + self.top_thickness, self.top_thickness, self.y - self.top_thickness*2)

    def switchHoles(self):
        spacing = self.x / self.switches_per_side
        for i in range(self.switches_per_side):
            self.hole(spacing*0.5 + spacing*i, self.switches_edge_distance, self.switch_diameter)

    def render(self):
        x, y, h = self.x, self.y, self.h
        t = self.thickness

        t1, t2, t3, t4 = "eeee"
        # b = self.edges.get(self.bottom_edge, self.edges["F"])
        b= "F"
        sideedge = "F" # if self.vertical_edges == "finger joints" else "h"

        if self.outside:
            self.x = x = self.adjustSize(x, sideedge, sideedge)
            self.y = y = self.adjustSize(y)
            self.h = h = self.adjustSize(h, b, t1)

        with self.saved_context():
            # self.rectangularWall(x, h, [b, sideedge, t1, sideedge],
            #                       move="up", callback=[None, None, None, self.xHoles])
            # self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
            #                       move="up", callback=[None, None, None, self.xHoles])

            self.rectangularWall(x, h, [b, sideedge, t1, sideedge],
                                  move="up", callback=[None, None, None, self.xHoles])
            self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                                  move="up", callback=[None, None, None, self.xHoles])  
            
            edges.DoveTailSettings.size = 3.5
            edges.DoveTailSettings.depth = 3
            edges.DoveTailSettings.angle = 50
            e = ["f", "e", edges.CompoundEdge(self, "DeD", [self.lip_width, x - self.lip_width*2, self.lip_width]), "e"]
            self.rectangularWall(x, self.lip_width,  e, move="up")
            self.rectangularWall(x, self.lip_width,  e, move="up")
                    

            if self.bottom_edge != "e":
                self.rectangularWall(x, y, "ffff", move="up")
            self.lid(x, y)
        
            self.rectangularWall(x, y, "eeee", move="up", callback=[self.switchHoles, None, self.switchHoles, None])

        self.rectangularWall(x, h, [b, sideedge, t3, sideedge],
                              move="right only")

        
       
        
        self.rectangularWall(y, h, [b, "f", t2, "f"],
                              move="up", callback=[None, None, None, self.yHoles])
        self.rectangularWall(y, h, [b, "f", t4, "f"],
                              move="up", callback=[None, None, None, self.yHoles])
        
        

        

        self.rectangularWall(y-self.lip_width*2, self.lip_width,  "fded", move="up")
        self.rectangularWall(y-self.lip_width*2, self.lip_width,  "fded", move="up")

        s = [self.pillar_width*0.5 - t*0.5, self.pillar_width*0.5 - t*0.5]
        e = [edges.SlottedEdge(self, s, "e", slots=0.5 * h), "e", "e", "e"]
        for i in range(self.number_of_pillars):
            self.rectangularWall(self.pillar_width, h, e, move= "right")
            self.rectangularWall(self.pillar_width, h, e, move= "right")

        

