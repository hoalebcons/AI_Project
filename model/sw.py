#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Switch"""

# from model.bridge import Bridge
from model.box import Box

class swQ:
    """Switch Bat Giac"""
    def __init__(self, symbol, typ, active, location, bridge=None):
        self.symbol = symbol
        self.type = typ
        self.active = active
        self.location = location
        self.bridge = bridge
    
    def set_bridge(self, bridge):
        self.bridge = bridge

    def change_active(self):
        self.active = not self.active
        if self.type == 0: 
            self.bridge.change_active()
            return True
        else:
            if self.bridge.check_times_active():
                return False
            else:
                self.bridge.change_active()
                return True
    
    def get_location(self):
        return self.location
    
    def get_bridge(self):
        return self.bridge

class swX:
    """Switch X"""
    def __init__(self, symbol, typ, active, location, bridge=None):
        self.symbol = symbol
        self.type = typ
        self.active = active
        self.location = location
        self.bridge = bridge
    
    def set_bridge(self, bridge):
        self.bridge = bridge

    def change_active(self):
        self.active = not self.active
        if self.type == 0: 
            self.bridge.change_active()
            return True
        else:
            if self.bridge.check_times_active():
                return False
            else:
                self.bridge.change_active()
                return True

    def get_location(self):
        return self.location
    
    def get_bridge(self):
        return self.bridge


class swO:
    """Switch tach doi"""
    def __init__(self, symbol, location, split, box1=None, box2=None):
        self.symbol = symbol
        self.location = location
        self.split = split
        self.box1 = box1
        self.box1 = box2
        self.active = 1
    
    def set_box1(self, symbol, state, location):
        self.box1 = Box(symbol, state, location)

    def set_box2(self, symbol, state, location):
        self.box2 = Box(symbol, state, location)

    def change_active(self):
        if self.active != 1:
            self.active == 1
            self.box1.on()
            self.box2.off()
        else: 
            self.active = 2
            self.box2.on()
            self.box1.off()

    def get_active_box(self):
        if self.active == 1:
            return self.box1
        else: return self.box2

    def get_all_box(self):
        return (self.box1, self.box2)

    def get_location(self):
        return self.location








    

    

