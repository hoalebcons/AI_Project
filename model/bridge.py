#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Bridge"""

class Bridge:
    def __init__(self, symbol, active, location):
        self.symbol = symbol
        self.times_active = 0
        self.active = active
        self.location = location
        self.type = len(location)

    def check_times_active(self):
        return self.times_active > 0
    
    def change_active(self):
        self.times_active += 1
        self.active = not self.active
        
