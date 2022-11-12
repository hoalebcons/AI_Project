import sys
from drawing.box import Box as Cube
from model.box import Box 
from copy import deepcopy
from model.map import maps as Maps
from model.tiles import tile as Tile
import math
import numpy as np

class Control:
    Play_handle = False
    def __init__(self, maps: Maps):
        if maps is None:
            print("Maps not None")
            sys.exit()
        
        # BOX
        self.start = maps.current_box.location
        self.current = maps.current_box.location
        
        # MAP
        self.maps = maps
        self.start_maps = self.maps.maps[:]
        self.curr_maps = self.start_maps
        self.size = maps.size

        self.stack = [(self.start, self.start_maps)] 
        self.visited = [(self.start, self.start_maps)]
        self.eval_maps = None
        self.curr_evaluate =  0
        self.end = [maps.end]
        
        self.moves = (self.move_up, self.move_down, self.move_right, self.move_left)

    def move_up(self):
        self.maps.current_box.move_up()
        if not self.check_box_on_maps():
            return False
        else:
            self.update_current_location()
            if not self.Play_handle:
                return self.add_stack() 
            return True 
    
    def move_down(self):
        self.maps.current_box.move_down()
        if not self.check_box_on_maps():
            return False
        else:
            self.update_current_location()
            if not self.Play_handle:
                return self.add_stack()  
            return True 
    
    def move_right(self):
        self.maps.current_box.move_right()
        if not self.check_box_on_maps():
            return False
        else:
            self.update_current_location()
            if not self.Play_handle:
                return self.add_stack()   
            return True 
    
    def move_left(self):
        self.maps.current_box.move_left()
        if not self.check_box_on_maps():
            return False
        else:
            self.update_current_location()
            if not self.Play_handle:
                return self.add_stack() 
            return True

    def update_current_location(self):
        self.current = self.maps.current_box.location
        self.curr_maps == self.maps.maps
        
    def update_box_locaton_for_maps(self, location):
        self.maps.current_box.location = location

    def check_box_on_maps(self):
        return self.maps.refreshBox()
    
    def set_state(self, state, maps):
        self.current = state
        self.curr_maps = deepcopy(maps)
        self.maps.maps = self.curr_maps
        self.maps.current_box.location = self.current
        
    def get_state(self):
        return deepcopy(self.current)
    
    def get_maps(self):
        return deepcopy(self.curr_maps)
    
    def add_stack(self):
        state = self.current
        maps = self.curr_maps
        self.stack.append((state, maps))
        return True
    
    def check_goal(self):
        return self.maps.check_goal()
    
    @staticmethod
    def Distance(pointA, pointB):
        X2 = math.pow(pointA[0]-pointB[0], 2)
        Y2 = math.pow(pointA[1]-pointB[1], 2)
        return math.sqrt(X2+Y2)

    def eval_func(self):
        goal = self.maps.end
        y , x =  self.size
        eval_maps = np.full((y, x), 0)
       
        for i in range(y):
            for j in range(x):
                delta = self.Distance([i,j], goal)
                eval_maps[i, j] = delta

        eval_maps[goal[0]][goal[1]] = 0

        self.eval_maps = eval_maps
        return eval_maps

    def evaluate(self):
        if len(self.current) == 2:
            point1, point2 = self.current
            self.curr_evaluate = (self.eval_maps[point1[0], point1[1]] + self.eval_maps[point2[0], point2[1]])/2
            return self.curr_evaluate
        elif len(self.current) == 1:
            point = self.current[0]
            self.curr_evaluate = self.eval_maps[point[0], point[1]]
            return self.curr_evaluate
    
    def get_evaluate(self):
        return self.curr_evaluate

    def set_evaluate(self, value):
        self.curr_evaluate = value
        
    def print_maps(self):
        self.maps.print_current()
    
    def draw_maps(self, path=None):
        height, width = self.size
        maps = self.curr_maps
        for x in range(width):
            for y in range(height):
                tile = maps[int(y)][int(x)]
                if tile.type != 0:
                    # if [y, x] in self.current or [y, x] in path:
                    #     Cube.draw_box(position=(x, y), size=(1, 1, -0.3), face_color=Tile.mark)
                    Cube.draw_box(position=(x, y), size=(1, 1, -0.3), face_color=tile.colors)
                else:
                    if tile.obj != None and tile.obj.symbol == "$":
                        Cube.draw_box(position=(x, y), size=(1, 1, -0.3), face_color=tile.colors)

    def draw_box(self):
        if len(self.current) == 2:
            current = self.current
        else: current = [self.current[0], self.current[0]]

        if self.maps.current_box.is_standing():
            Cube.draw_box(position=(current[0][1], current[0][0]), size=(1, 1, 2), border_color=(0.8, 0.8, 0.8))
        elif self.maps.current_box.is_vertical():
            Cube.draw_box(position=(current[1][1], current[1][0]), size=(1, 2, 1), border_color=(0.8, 0.8, 0.8))
        elif self.maps.current_box.is_horizontal():
            Cube.draw_box(position=(current[0][1], current[0][0]), size=(2, 1, 1), border_color=(0.8, 0.8, 0.8))
    
    def draw_StartBox(self):
        if len(self.start) == 2:
            current = self.start
        else: current = [self.start[0], self.start[0]]
        
        BoxStart = Box("#", len(self.start), self.start)

        if BoxStart.is_standing():
            Cube.draw_box(position=(current[0][1], current[0][0]), size=(1, 1, 2), border_color=(0.8, 0.8, 0.8))
        elif BoxStart.is_vertical():
            Cube.draw_box(position=(current[1][1], current[1][0]), size=(1, 2, 1), border_color=(0.8, 0.8, 0.8))
        elif BoxStart.is_horizontal():
            Cube.draw_box(position=(current[0][1], current[0][0]), size=(2, 1, 1), border_color=(0.8, 0.8, 0.8))
    
    def draw_StartMaps(self):
        height, width = self.size
        maps = self.start_maps
        for x in range(width):
            for y in range(height):
                tile = maps[int(y)][int(x)]
                if tile.type != 0:
                    Cube.draw_box(position=(x, y), size=(1, 1, -0.3), face_color=tile.colors)