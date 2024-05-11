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
from math import tan, radians, cos, sin

class SolenoidArm(Boxes):
    """Fully closed box"""

    ui_group = "Box"

    

    description = """This box is more of a building block than a finished item.
Use a vector graphics program (like Inkscape) to add holes or adjust the base
plate.

See BasedBox for variant with a base."""

    def __init__(self) -> None:
        Boxes.__init__(self)
        self.addSettingsArgs(edges.FingerJointSettings)
        self.buildArgParser("x", "y", "h", "outside")
        
        self.argparser.add_argument(
            "--solenoid_mounting_holes_width",
            action="store",
            type=float,
            default=12,
            help="Distance between mounting holes(x)",
        )
        self.argparser.add_argument(
            "--solenoid_mounting_holes_height",
            action="store",
            type=float,
            default=15,
            help="Distance between mounting holes(y)",
        )
        self.argparser.add_argument(
            "--solenoid_mounting_holes_diameter",
            action="store",
            type=float,
            default=3,
            help="Diameter of mounting holes",
        )
        self.argparser.add_argument(
            "--solenoid_distance_to_hole",
            action="store",
            type=float,
            default=12.5,
            help="Distance from edge of solenoid to actuator hole",
        )
        self.argparser.add_argument(
            "--arm_angle",
            action="store",
            type=float,
            default=50,
            help="Angle of arm",
        )
        self.argparser.add_argument(
            "--arm_width",
            action="store",
            type=float,
            default=10,
            help="Width of arm",
        )
        # self.argparser.add_argument(
        #     "--arm_length",
        #     action="store",
        #     type=float,
        #     default=80,
        #     help="Length of arm",
        # )
        self.argparser.add_argument(
            "--arm_offset",
            action="store",
            type=float,
            default=18.5,
            help="x distance of solenoid actuator hole from centre of mounting holes",
        )
        self.argparser.add_argument(
            "--arm_bridge_length",
            action="store",
            type=float,
            default=0,
            help="Length of bridge between arms",
        )
        self.argparser.add_argument(
            "--arm_hole_diameter",
            action="store",
            type=float,
            default=3,
            help="Diameter of arm hole",
        )
        
        self.argparser.add_argument(
            "--lever_x",
            action="store",
            type=float,
            default=100,
            help="Length of top of lever",
        )
        self.argparser.add_argument(
            "--lever_width",
            action="store",
            type=float,
            default=8,
            help="Width of lever",
        )
        self.argparser.add_argument(
            "--solenoid_actuator_hole",
            action="store",
            type=float,
            default=3,
            help="diameter of hole in solenoid actuator",
        )
        self.argparser.add_argument(
            "--solenoid_axle_hole",
            action="store",
            type=float,
            default=3,
            help="diameter of bolt for lever axle",
        )
        self.argparser.add_argument(
            "--lever_inset_distance",
            action="store",
            type=float,
            default=2,
            help="amount of lever inset",
        )
        self.argparser.add_argument(
            "--lever_inset_length",
            action="store",
            type=float,
            default=15,
            help="length of lever inset section",
        )
        self.argparser.add_argument(
            "--lever_hole_extra",
            action="store",
            type=float,
            default=5,
            help="amount of extra space for the solenoid hole",
        )
        self.argparser.add_argument(
            "--lever_angle",
            action="store",
            type=float,
            default=0,
            help="",
        )
        self.argparser.add_argument(
            "--lever_thickness",
            action="store",
            type=float,
            default=2,
            help="",
        )
        self.argparser.add_argument(
            "--circle_diameter",
            action="store",
            type=float,
            default=25,
            help="",
        )
        self.argparser.add_argument(
            "--circle_inside_diameter",
            action="store",
            type=float,
            default=13,
            help="",
        )

    def baseFingerHoles(self):
            self.fingerHolesAt(-self.thickness+self.x/2-self.thickness, -self.thickness, self.longerY, 90)
            self.fingerHolesAt(-self.thickness+self.x/2+self.thickness, -self.thickness, self.longerY, 90)
            
    def baseOuterHoles(self):
         self.hole(-self.thickness+self.x/2 + self.solenoid_mounting_holes_width/2, -self.thickness+self.y/2 + self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
         self.hole(-self.thickness+self.x/2 + self.solenoid_mounting_holes_width/2, -self.thickness+self.y/2 - self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
         self.hole(-self.thickness+self.x/2 - self.solenoid_mounting_holes_width/2, -self.thickness+self.y/2 + self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
         self.hole(-self.thickness+self.x/2 - self.solenoid_mounting_holes_width/2, -self.thickness+self.y/2 - self.solenoid_mounting_holes_height/2, d=self.solenoid_mounting_holes_diameter)
        
    def baseInsideCallbacks(self):
        self.baseFingerHoles()
        self.baseOuterHoles()
        self.baseLeverHole()

    def armEndHole(self):
        self.hole(self.arm_width/2, self.arm_width/2, d=self.arm_hole_diameter)
    
    def leverBottomHole(self):
        #  self.rectangularHole(self.lever_width/2, self.lever_width/2 + self.lever_hole_extra/2, self.solenoid_actuator_hole,  self.solenoid_actuator_hole + self.lever_hole_extra)
         self.rectangularHole(self.lever_width/2, self.lever_width/2 + self.lever_hole_extra/2, self.solenoid_actuator_hole,  self.solenoid_actuator_hole + self.lever_hole_extra, r=self.solenoid_actuator_hole/2)

    def leverTopHole(self):
         self.hole(-self.lever_width/2, self.lever_width/2, d=self.solenoid_axle_hole)

    def armFingerHoles(self):
         self.fingerHolesAt(-self.arm_width/2, self.arm_width/2, self.arm_bridge_length, 0)
    
    def leverSquareHole(self):
        # self.rectangularHole(self.lever_width/2, self.lever_width/2, self.lever_width/2, self.lever_width/2)
        self.rectangularHole(self.thickness/2, 20, self.thickness, self.thickness)
        self.rectangularHole(self.thickness/2, 80, self.thickness, self.thickness)

    def baseLeverHole(self):
        len = self.solenoid_distance_to_hole + self.lever_width/2 + 2
        self.rectangularHole(self.x/2-self.thickness, -self.thickness-len/2, self.thickness, len)

    def circleCutout(self):
        ht = self.circle_diameter/2 - self.circle_inside_diameter/2 - self.thickness + 1
        self.rectangularHole(0,  -ht/2 -self.circle_inside_diameter/2 - self.thickness, self.lever_thickness, ht)

    def render(self):

        x, y, h = self.x, self.y, self.h

        if self.outside:
            x = self.adjustSize(x)
            y = self.adjustSize(y)
            h = self.adjustSize(h)

        t = self.thickness

        d2 = edges.Bolts(2)
        d3 = edges.Bolts(3)

        d2 = d3 = None

        a = self.arm_width * sin(radians(90-self.arm_angle))
        b = self.arm_width - a
        c = b / cos(radians(90-self.arm_angle))

        self.longerY = self.y * 2
        
        

        self.rectangularWall(x, y*2, ["E", "E", "E", "E"], bedBolts=[d2, d3, d2, d3], callback= [self.baseInsideCallbacks] ,move="right", label="Base")
        


        offset = (tan(radians(self.arm_angle)) * self.arm_width/2)

        lengthOffset = offset + self.arm_width/2
        targetX = self.arm_offset - self.y/2
        self.arm_length = targetX / cos(radians(self.arm_angle)) + lengthOffset

        short_arm_length = self.arm_length - (tan(radians(self.arm_angle)) * self.arm_width)


        adj = self.arm_length - self.arm_width/2 - offset
        self.height_to_arm_hole = tan(radians(self.arm_angle)) * adj + cos(radians(self.arm_angle)) * self.arm_width/2 # plus thickness + solenoid distance
        self.height_to_arm_hole = sin(radians(self.arm_angle)) * short_arm_length
        self.lever_hole_length = self.height_to_arm_hole + self.thickness + self.solenoid_distance_to_hole

        self.polygonWall([self.arm_width, 90, self.longerY, self.arm_angle, self.arm_length, 90, self.arm_width, 90, self.arm_length - c, -self.arm_angle, None], "efeeeeee", callback=[None, None, self.armFingerHoles, self.armEndHole], label="arm", move="right")
        self.polygonWall([self.arm_width, 90, self.longerY, self.arm_angle, self.arm_length, 90, self.arm_width, 90, self.arm_length - c, -self.arm_angle, None], "efeeeeee", callback=[None, None, self.armFingerHoles, self.armEndHole], label="arm", move="right")

        self.rectangularWall(self.arm_bridge_length, self.thickness, "fefe", label="Arm bridge", move="")

        edges.StackableSettings.height = 1
        edges.StackableSettings.width = 2
        self.lever_height_adjusted = self.lever_hole_length + self.lever_width + self.lever_hole_extra
        self.lever_x_adjusted = (self.lever_x - self.lever_width) /2

        diagonal_length = self.lever_inset_distance/ cos(radians(45))
        
        lever_dist = self.lever_inset_length - self.lever_inset_distance*2
        self.polygonWall([self.lever_width, 90, self.lever_height_adjusted, -45, diagonal_length, self.lever_angle-45, lever_dist, -45, diagonal_length, 45, self.lever_x_adjusted - self.lever_inset_length, 90,
                           self.lever_width, 90, self.lever_x, 90, self.lever_width,   90, self.lever_x_adjusted, -90,
                             self.lever_height_adjusted, 90], 
                               "e",#ešeeeše",
                                 label="lever", move="right", callback=[self.leverBottomHole, None, None, None, None, None, None, None, self.leverSquareHole, None, self.leverTopHole])
        
        self.parts.disc(self.circle_diameter, self.circle_inside_diameter, move="right", callback=self.circleCutout)
        self.rectangularWall(6,1.5,"eeee")
# ajd * tan(angle)

