# road_track.py        
"""
Basis of a road network
Uses RoadBlock parts
"""
from enum import Enum
import copy
from homcoord import *


from select_trace import SlTrace
from select_error import SelectError

from block_block import BlockBlock,BlockType
from block_polygon import BlockPolygon
from road_block import RoadBlock,SurfaceType
from road_strait import RoadStrait

   
class RoadTrack(BlockBlock):
    """
    Road track 
    which can be used to construct a road layout
    Object properties are expressed in relation to the containing object.
    """
    
            
    def __init__(self,
                canvas=None,
                cv_width=None,
                cv_height=None,
                road_width=.05,
                road_length=.05*2,
                surface=SurfaceType.DEFAULT,
                **kwargs
                ):
        """ Setup object
        :road_width: road width as a fraction of track's width dimensions'
                e.g. 1,1 with container==None ==> block is whole canvas
        :road_length: road width as a fraction of track's width dimensions'
                e.g. 1,1 with container==None ==> block is whole canvas
        :surface: road surface type - determines look and operation/handeling                                                    collisions)
        """
        SlTrace.lg("RoadTrack: %s" % (self))
        if canvas is None:
            canvas = Canvas(width=cv_width, height=cv_height)
        self.cv_width = cv_width
        self.cv_height = cv_height
        super().__init__(**kwargs)
        self.canvas = canvas    
        self.roads = []     # List of components    # Parts of track
        self.road_width = road_width
        self.road_length = road_length
        self.surface = surface
        """ Do background / sceenery
        """
        bk_inset = .001
        p1 = Pt(0,0)
        p2 = Pt(0,1)
        p3 = Pt(1,1)
        p4 = Pt(1,0)
        bkground = BlockPolygon(tag="track_background",
                              points=[p1,p2,p3,p4], position=Pt(bk_inset,bk_inset),
                              container=self,
                              ctype=BlockType.POLYGON,
                              height = 1.0 - 2*bk_inset,
                              width = 1.0 - 2*bk_inset,
                              xkwargs={'fill':'lightgreen'})
        self.comps.append(bkground)
        
    
    def add_roads(self, roads):
        """ Add one or more road parts
        :roads: one or list of components
        """
        if not isinstance(roads, list):
            roads = [roads]
        self.roads.extend(roads)

    
    def display(self):
        """ Display thing as a list of components
        """
        if self.canvas is not None:
            self.canvas.update_idletasks()
            self.canvas.update()
        
        """ Do background / sceenery
        """
        for comp in self.comps:
            comp.display() 
        for road in self.roads:
            road.display()

    def get_canvas(self):
        return self.canvas

    def get_cv_width(self):
        return self.cv_width
    
    def get_cv_height(self):
        return self.cv_height;

    def get_road_surface(self):
        return self.surface
        

    def get_road_width(self):
        """ Get road width in pixels
        """
        w = self.road_width * width
        wpi = w * self.cv_width
        return wpi
        

    def get_road_length(self):
        """ Get road length in pixels
        """
        l = self.road_length * width    # Scale against track/canvas width
        lpi = l * self.cv_width
        return lpi
        

    def get_road_rotation(self):
        """ Get road rotation in degrees
        Adds in  container or track rotation if any
        :returns: None if no rotation
        """
        return self.rotation
    
        
if __name__ == "__main__":
    import os
    import sys
    from tkinter import *    
    import argparse
    
    from road_block import RoadBlock
    from road_turn import RoadTurn
    from block_arc import BlockArc

    
    
    width = 600     # Window width
    height = width  # Window height
    rotation = None # No rotation
    pos_x = None
    pos_y = None
    parser = argparse.ArgumentParser()
    dispall = False      # Display every change
    
    parser.add_argument('--width=', type=int, dest='width', default=width)
    parser.add_argument('--height=', type=int, dest='height', default=height)
    parser.add_argument('--pos_x=', type=float, dest='pos_x', default=pos_x)
    parser.add_argument('--pos_y=', type=float, dest='pos_y', default=pos_y)
    parser.add_argument('--rotation=', type=float, dest='rotation', default=rotation)
    args = parser.parse_args()             # or die "Illegal options"
    
    width = args.width
    height = args.height
    pos_x = args.pos_x
    pos_y = args.pos_y
    rotation = args.rotation
    
    SlTrace.lg("%s %s\n" % (os.path.basename(sys.argv[0]), " ".join(sys.argv[1:])))
    SlTrace.lg("args: %s\n" % args)
    
            
    frame = Frame(width=width, height=height, bg="", colormap="new")
    frame.pack()
    canvas = Canvas(frame, width=width, height=height)
    canvas.pack()   
    th_width = 1.
    th_height = 1.
    position = None
    if pos_x is not None or pos_y is not None:
        if pos_x is None:
            pos_x = 0.
        if pos_y is None:
            pos_y = 0.
        position = Pt(pos_x, pos_y)
        
    tR = RoadTrack(tag="road_track",
                   canvas=canvas, width=th_width, height=th_height,
                   position=position,
                   cv_width=width, cv_height=height,
                   rotation=rotation)
    tR.display()

    turn_arc = 90
    rot1 = -10.
    pos1 = Pt(.5, .25)
    strait_road1 = RoadStrait(tR, tag="first_road",
                             rotation=rot1,
                             position=pos1)
    tR.add_roads(strait_road1)    
    if dispall: tR.display()
    
    corn_rot1 = rot1
    corn_pos1 = strait_road1.get_top_left()
    turn_road1 = RoadTurn(tR, tag="road_turn1",
                             arc=turn_arc,
                             rotation=corn_rot1,
                             position=corn_pos1)
    tR.add_roads(turn_road1)
        
    strait_after_turn1 = RoadStrait(tR, tag="after_turn",
                             rotation=corn_rot1+turn_arc,
                             ###position=turn_road1.get_top_left())
                             position=strait_road1.get_top_left())      #Hack
    tR.add_roads(strait_after_turn1)
    
    extend_rot1 = rot1
    extend_pos1 = strait_road1.get_relative_point(Pt(0,-1))     # before
    ###extend_pos1 = strait_road1.get_relative_point(Pt(1,1))      # up to right
    extend_road1 = RoadStrait(tR, tag="road_extend5",
                             rotation=extend_rot1,
                             position=extend_pos1)
    tR.add_roads(extend_road1)
     
    cir_pos = Pt(.9,.9)
    cir_pi_x = 0
    cir_pi_y = -.1
    circle1 = BlockArc(container=tR, tag="cirlce", radius=.05, arc=360., position=cir_pos)
    tR.comps.append(circle1)
    

    cir_pos = Pt(cir_pos.x+cir_pi_x, cir_pos.y+cir_pi_y)
    circle1 = BlockArc(container=tR, tag="cirlce", radius=.05, rotation=30, arc=360., position=cir_pos)
    tR.comps.append(circle1)

    cir_pos = Pt(cir_pos.x+cir_pi_x, cir_pos.y+cir_pi_y)
    circle1 = BlockArc(container=tR, tag="cirlce3", radius=.03, arc=90., position=cir_pos)
    tR.comps.append(circle1)
    
    cir_pos = Pt(cir_pos.x+cir_pi_x, cir_pos.y+cir_pi_y)
    circle1 = BlockArc(container=tR, tag="cirlce3", radius=.03, arc=180., position=cir_pos)
    tR.comps.append(circle1)
    
    cir_pos = Pt(cir_pos.x+cir_pi_x, cir_pos.y+cir_pi_y)
    circle1 = BlockArc(container=tR, tag="cirlce3", radius=.03, rotation=30, arc=180., position=cir_pos)
    tR.comps.append(circle1)
    
    cir_pos = Pt(cir_pos.x+cir_pi_x, cir_pos.y+cir_pi_y)
    circle1 = BlockArc(container=tR, tag="cirlce2", radius=.025, arc=270., position=cir_pos)
    tR.comps.append(circle1)
    
    cir_pos = Pt(cir_pos.x+cir_pi_x, cir_pos.y+cir_pi_y)
    circle1 = BlockArc(container=tR, tag="cirlce2", radius=.025, rotation=30, arc=270., position=cir_pos)
    tR.comps.append(circle1)
        
    if dispall: tR.display()

    
    rot2 = 30.
    pos2 = Pt(.1, .2)
    strait_road2 = RoadStrait(tR, tag="second_road",
                             rotation=rot2,
                             position=pos2)
    tR.add_roads(strait_road2)    
    if dispall: tR.display()
    
    corn_rot2 = rot2
    corn_pos2 = strait_road2.get_top_left()
    turn_road2 = RoadTurn(tR, tag="road_turn",
                             arc=turn_arc,
                             rotation=corn_rot2,
                             position=corn_pos2)
    tR.add_roads(turn_road2)    
    if dispall: tR.display()
    
    extend_rot2 = rot2
    extend_pos2 = strait_road2.get_relative_point(Pt(0,-1))     # before
    extend_road2 = RoadStrait(tR, tag="road_extend2",
                             rotation=extend_rot2,
                             position=extend_pos2)
    tR.add_roads(extend_road2)    
    if dispall: tR.display()

    
    rot3 = 90.
    pos3 = Pt(.75, .75)
    strait_road3 = RoadStrait(tR, tag="road3",
                             rotation=rot3,
                             position=pos3)
    tR.add_roads(strait_road3)    
    if dispall: tR.display()
    
    corn_rot3 = rot3
    corn_pos3 = strait_road3.get_relative_point(Pt(0,1))
    turn_road3 = RoadTurn(tR, tag="road_turn",
                             arc=turn_arc,
                             rotation=corn_rot3,
                             position=corn_pos3)
    tR.add_roads(turn_road3)    
    if dispall:  tR.display()
    
    extend_rot3 = rot3
    extend_pos3 = strait_road3.get_relative_point(Pt(0,-1))     # before
    extend_road3 = RoadStrait(tR, tag="road_extend3",
                             rotation=extend_rot3,
                             position=extend_pos3)
    tR.add_roads(extend_road3)    
    if dispall: tR.display()

    
    rot4 = 135.
    pos4 = Pt(.25, .75)
    strait_road4 = RoadStrait(tR, tag="road4",
                             rotation=rot4,
                             position=pos4)
    tR.add_roads(strait_road4)    
    if dispall:  tR.display()
    
    corn_rot4 = rot4
    corn_pos4 = strait_road4.get_top_left()
    turn_road5 = RoadTurn(tR, tag="road_turn4",
                             arc=turn_arc,
                             rotation=corn_rot4,
                             position=corn_pos4)
    tR.add_roads(turn_road5)    
    if dispall:  tR.display()
    
    extend_rot4 = rot4
    extend_pos4 = strait_road4.get_relative_point(Pt(0,-1))     # before
    extend_road4 = RoadStrait(tR, tag="road_extend4",
                             rotation=extend_rot4,
                             position=extend_pos4)
    tR.add_roads(extend_road4)    
    if dispall:  tR.display()
 
    
    rot5 = 30.
    pos5 = Pt(.5, .5)
    strait_road5 = RoadStrait(tR, tag="road5",
                            rotation=rot5,
                            position=pos5)
    tR.add_roads(strait_road5)    
    if dispall: tR.display()
    
    corn_rot5 = rot5
    corn_pos5 = strait_road5.get_top_left()
    turn_road5 = RoadTurn(tR, tag="road_turn5",
                             arc=turn_arc,
                             rotation=corn_rot5,
                             position=corn_pos5)
    tR.add_roads(turn_road5)    
    if dispall: tR.display()
    
    extend_rot5 = rot5
    extend_pos5 = strait_road5.get_relative_point(Pt(0,-1))     # before
    extend_road5 = RoadStrait(tR, tag="road_extend5",
                             rotation=extend_rot5,
                             position=extend_pos5)
    tR.add_roads(extend_road5)    
    tR.display()
    
    mainloop()