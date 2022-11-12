#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Map"""
import simplejson as json
from model.sw import swO, swQ, swX
from model.box import Box
from model.bridge import Bridge
from model.tiles import tile
class goal:
    def __init__(self, symbol, location):
        self.symbol = symbol
        self.location = location
        
class maps:
    def __init__(self, path_to_level=None):
        self.files = None
        self.jsonObj = None
        self.maps = list()
        self.level = None
        self.size = None
        self.start = None
        self.end = None 
        self.current_box = None
        self.types_tile = None
        self.swQ = list()
        self.swX = list()
        self.swO = list()
        self.Brid = list()
        if path_to_level != None:
            self.loadLevel(path_to_level)

    def loadLevel(self, path_to_level=None):
        if path_to_level != None:
            self.files = open(path_to_level, "r")
            self.jsonObj = json.loads(self.files.read())

            # Name Level
            self.level = self.jsonObj["level"]
            # Size Map
            self.size = self.jsonObj["size"]
            # Start Location
            self.start = self.jsonObj["start"]
            # End Location
            self.end = self.jsonObj["end"]
            # Types of tiles
            self.types_tile = [self.jsonObj["tiles"]["orange"], self.jsonObj["tiles"]["rock"], self.jsonObj["tiles"]["space"]]
            # Current Box
            boxObj = self.jsonObj["box"]
            self.current_box = Box(boxObj["symbol"], boxObj["state"], boxObj["location"])
            # Load swX
            self.__loadSWX()
            # Load swQ
            self.__loadSWQ()
            # Load swO
            # self.__loadSWO()
            # Load Maps
            self.__loadMap()
            # Update Maps
            self.updateMaps()

        else: print("Path_to_level not None")
    
    def __loadMap(self):
        # Load tiles to Maps
        maps = self.jsonObj["maps"]
        for i in range(self.size[0]):
            line = []
            for j in range(self.size[1]):
                if maps[i][j] == self.types_tile[0]: # orange tile
                    newtile = tile(2, None, [i, j])
                    line.append(newtile)
                elif maps[i][j] == self.types_tile[1]: # rock tile
                    newtile = tile(1, None, [i, j])
                    line.append(newtile)
                elif maps[i][j] == self.types_tile[2]: # space title
                    newtile = tile(0, None, [i, j])
                    if self.end == [i, j]:
                        newtile.set_obj(goal("$", [i, j])) # End game
                    line.append(newtile)
                else:
                    newtile = tile(1, None, [i, j])
                    line.append(newtile)
            self.maps.append(line)

    def updateMaps(self):
        # Load swO to Maps
        if len(self.swO) != 0:
            for child in self.swO:
                self.maps[int(child.location[0])][int(child.location[1])].set_obj(child)
        # Load swQ to Maps
        if len(self.swQ) != 0:
            for child in self.swQ:
                self.maps[int(child.location[0])][int(child.location[1])].set_obj(child)
        # Load swX to Maps
        if len(self.swX) != 0:
            for child in self.swX:
                self.maps[int(child.location[0])][int(child.location[1])].set_obj(child)

        if len(self.Brid) != 0:
            for child in self.Brid:
                if child.type == 1: # child tile
                    if child.active == True:
                        self.maps[int(child.location[0][0])][int(child.location[0][1])].type = 1
                    else: 
                        self.maps[int(child.location[0][0])][int(child.location[0][1])].type = 0
                    self.maps[int(child.location[0][0])][int(child.location[0][1])].set_obj(child)
                elif child.type == 2: # Two tile
                    if child.active == True:
                        self.maps[int(child.location[0][0])][int(child.location[0][1])].type = 1
                    else: 
                        self.maps[int(child.location[0][0])][int(child.location[0][1])].type = 0
                    self.maps[int(child.location[0][0])][int(child.location[0][1])].set_obj(child)
 
                    if child.active == True:
                        self.maps[int(child.location[1][0])][int(child.location[1][1])].type = 1
                    else: 
                        self.maps[int(child.location[1][0])][int(child.location[1][1])].type = 0
                    self.maps[int(child.location[1][0])][int(child.location[1][1])].set_obj(child)
    
    def refreshBox(self):
        if not self.__onFloor(self.current_box):
            self.current_box.location = self.current_box.pre_location
            return False
        return True

    def checkSWQ(self):
        for child in self.current_box.location:
            y, x = child
            if type(self.maps[y][x].obj) is swQ:
                if self.maps[y][x].obj.change_active():
                    self.__updateSWQ(self.maps[y][x].obj)
                
    def checkSWX(self):
        for child in self.current_box.location:
            y, x = child
            if type(self.maps[y][x].obj) is swX:
                if self.current_box.is_doubleBox() and self.current_box.is_standing():
                    if self.maps[y][x].obj.change_active():
                        self.__updateSWX(self.maps[y][x].obj)

    def __updateSWX(self, swXObj):
        for child in self.swX:
            if child.symbol == swXObj.symbol:
                self.swX[self.swX.index(child)].active = swXObj.active
                self.__updateBrid(swXObj.bridge)
    
    def __updateSWQ(self, swQObj):
        for child in self.swQ:
            if child.symbol == swQObj.symbol:
                self.swQ[self.swQ.index(child)].active = swQObj.active
                self.__updateBrid(swQObj.bridge)
    
    def __updateSWO(self, swOObj):
        for child in self.swO:
            if child.symbol == swOObj.symbol:
                self.swO[self.swO.index(child)] = swOObj
                self.updateMaps()
    
    def __is_goal(self):
        return self.end == self.current_box.location[0]

    def check_goal(self):
        return self.current_box.is_standing() and self.current_box.is_doubleBox() and self.__is_goal()
     
    def __is_valid(self, box):
        self.checkSWQ()
        self.checkSWX()
        if len(box.location) == 1:
            y , x = box.location[0]
            return self.maps[y][x].check_material_tile(box)
        elif len(box.location) == 2:
            for child in box.location:
                y, x = child
                if not self.maps[y][x].check_material_tile(box): 
                    return False
            return True
    
    def __onFloor(self, box):
        width, height = self.size
        if len(box.location) == 1:
            y, x = box.location[0]
            if y < 0 or y >= width or x < 0 or x >= height:
                return False
            return self.__is_valid(box)
        elif len(box.location) == 2:
            for child in box.location:
                y , x = child
                if y < 0 or y >= width or x < 0 or x >= height:
                    return False
            return self.__is_valid(box)

    def __updateBrid(self, bridObj):
        index = bridObj.location
        if bridObj.type == 1:
            if bridObj.active:
                self.maps[index[0][0]][index[0][1]] = tile(1, bridObj, index[0])
            else:
                self.maps[index[0][0]][index[0][1]] = tile(0, bridObj, index[0])
        elif bridObj.type == 2:
            if bridObj.active:
                self.maps[index[0][0]][index[0][1]] = tile(1, bridObj, index[0])
                self.maps[index[1][0]][index[1][1]] = tile(1, bridObj, index[1])
            else:
                self.maps[index[0][0]][index[0][1]] = tile(0, bridObj, index[0])
                self.maps[index[1][0]][index[1][1]] = tile(0, bridObj, index[1])

    def __loadSWX(self):
        swXObj = self.jsonObj["swX"]
        count = int(swXObj["count"])
        if count > 0:
            symbol = swXObj["symbol"]
            for sym in symbol:
                symObj = swXObj[sym]
                newswX = swX(sym, symObj["type"], symObj["active"], symObj["location"])
                bridObj = self.jsonObj["bridge"]
                nameBrid = symObj["bridge"]
                if int(bridObj["count"]) > 0:
                    chidBrid = bridObj[nameBrid]
                    newBrid = Bridge(nameBrid, chidBrid["active"], chidBrid["location"])
                    newswX.set_bridge(newBrid)
                    self.Brid.append(newBrid)
                self.swX.append(newswX)

    def __loadSWQ(self):
        swQObj = self.jsonObj["swQ"]
        count = int(swQObj["count"])
        if count > 0:
            symbol = swQObj["symbol"]
            for sym in symbol:
                symObj = swQObj[sym]
                newswQ = swQ(sym, symObj["type"], symObj["active"], symObj["location"])
                bridObj = self.jsonObj["bridge"]
                nameBrid = symObj["bridge"]
                if int(bridObj["count"]) > 0:
                    chidBrid = bridObj[nameBrid]
                    newBrid = Bridge(nameBrid, chidBrid["active"], chidBrid["location"])
                    newswQ.set_bridge(newBrid)
                    self.Brid.append(newBrid)
                self.swQ.append(newswQ)
    
    def __loadSWO(self):
        swOObj = self.jsonObj["swO"]
        count = int(swOObj["count"])
        if count > 0:
            symbol = swOObj["symbol"]
            for sym in symbol:
                symObj = swOObj[sym]
                newswO = swO(sym, symObj["location"], symObj["split"])
                box1, box2 =  symObj["box1"], symObj["box2"]
                newswO.set_box1(box1["symbol"], box1["state"], box1["location"])
                newswO.set_box2(box2["symbol"], box2["state"], box2["location"])
                self.swO.append(newswO)

    def print_current(self):
        for i in self.maps:
            print("------" * self.size[1])
            print('{0: <3}'.format("|"), end='')
            for j in i:
                if j.type == 0:
                    content = " "
                    if j.obj != None:
                        if j.obj.symbol == "$":
                            content = "$"
                elif j.type == 1 or j.type == 2:
                    if j.obj != None:
                        content = j.obj.symbol
                    else: content = j.type
                if j.location in self.current_box.location:
                    content = "#"
                print('{0: <2}'.format(content),"|", end='')
                print('{0: <2}'.format(""), end='')
            print("\n",end='')
        print("------" * self.size[1])

    
