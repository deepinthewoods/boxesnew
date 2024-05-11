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


class DrumStick(Boxes):
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
            "--number_of_guides",
            action="store",
            type=int,
            default=12,
            help="",
        )
        self.argparser.add_argument(
            "--guide_length",
            action="store",
            type=float,
            default=30,
            help="",
        )
        self.argparser.add_argument(
            "--guide_height",
            action="store",
            type=float,
            default=16,
            help="",
        )

    def fingerHolesTop(self):
        self.fingerHolesAt(self.y*0.5, -self.thickness, self.x)

    def render(self):

        x, y, h = self.x, self.y, self.h

        if self.outside:
            x = self.adjustSize(x)
            # y = self.adjustSize(y)
            h = self.adjustSize(h)

        t = self.thickness

        d2 = edges.Bolts(2)
        d3 = edges.Bolts(3)

        d2 = d3 = None

        self.rectangularWall(x, h, "EEfE", bedBolts=[d2] * 4, move="down", label="Wall 1")

        self.rectangularWall(x, y, "eeee", bedBolts=[d3, d2, d3, d2], move="down", label="top", callback = [None, self.fingerHolesTop, None, None])

        self.rectangularWall(self.guide_length, self.guide_height, "efee", bedBolts=[d3, d2, d3, d2], move="down right", label="guide")
        self.rectangularWall(self.guide_length, self.guide_height, "efee", bedBolts=[d3, d2, d3, d2], move="right", label="guide")

        self.rectangularWall(self.thickness, self.guide_height, "eFeF", bedBolts=[d3, d2, d3, d2], move="right", label="guide")
        



