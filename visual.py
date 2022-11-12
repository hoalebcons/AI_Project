import pygame
import sys
import os
import time
from drawing.display import Display
from model.map import maps
from model.control import Control

class Level:
    lv1  = "./level/1.json"
    lv2 = "./level/2.json"
    lv3 = "./level/3.json"
    lv4 = "./level/4.json"
    lv5 = "./level/5.json"
    lv6 = "./level/6.json"
    lv7 = "./level/7.json"
    lv8 = "./level/8.json"
    lv9 = "./level/9.json"
    lv10 = "./level/10.json"
    lv11 = "./level/11.json"
    lv12 = "./level/12.json"
    lv13 = "./level/13.json"
    lv14 = "./level/14.json"
    lv15 = "./level/15.json"

def flatMap(path):
    return [y for x in path for y in x]


def convert(state: Control, solution):
    result = [state.start]

    for move in solution:
        
        current_state, current_maps = state.stack.pop()
        state.set_state(current_state, current_maps)

        if move == "U":
            state.move_up()
        elif move == "D":
            state.move_down()
        elif move == "R":
            state.move_right()
        elif move == "L":
            state.move_left()
        
        result = result + [state.current]
                    
    return result

def draw_path_3D(solution, timesleep=0.5, level=Level.lv1, map_size = (0,0)):
    pygame.init()
    display = Display(title='Bloxorz Game', map_size=map_size)
    if solution != None:
        
        print("Let's play")
        choiselv = maps(level)

        level = Control(choiselv)
        level.draw_StartBox()
        level.draw_StartMaps()
        display.update() 

        for path in solution:
            time.sleep(timesleep)
            level.current = path
            level.update_box_locaton_for_maps(path)
            
            if level.maps.refreshBox():
                level.update_current_location()
            else: 
                print("Fail!")
                return

            level.draw_box() 
            level.draw_maps()   
            display.update()
        return
    else:
        print("Unable to find path!")
        return

    
def run(level=Level.lv1, solution = ""):
    Maps = maps(level)
    size = Maps.size
    state = Control(Maps) 
    result = convert(state, solution)
    draw_path_3D(result, level=level, map_size=(size[0], size[1]))
    time.sleep(1)
    sys.exit()

if __name__=="__main__":
    
    level = sys.argv[1]
    #solution = input("Enter the solution: ")
    solution = "DLURRRRRDRLULLLLLDRDRDRRRUURDLURUURRRDRDRDLU" 
    run(level=level, solution=solution)
    