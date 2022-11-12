from model.direction import Direction

"""Box"""
class Box:
    def __init__(self, symbol, state, location):
        self.symbol = symbol
        self.state = state
        self.active = False
        self.location = location
        self.pre_location = location

    def change_state(self, state):
        self.state = state

    def move_up(self):
        numGPS = len(self.location)
        if self.state == 2:
            # Nam dung
            if numGPS == 1:
                yi, xi = self.location[0]
                newYi1, newYi2  = int(yi-1), int(yi-2)
                newLocation = [[newYi1, xi],[newYi2, xi]]
                self.change_location(newLocation)
            else:
                # Nam ngang
                if self.is_horizontal():
                    y1, x1 = self.location[0]
                    y2, x2 = self.location[1]
                    newY1, newY2 = int(y1-1), int(y2-1)
                    newLocation = [[newY2, x1], [newY1, x2]]
                    self.change_location(newLocation)
                # Nam Doc
                elif self.is_vertical():
                    yi, xi = self.location[1]
                    newYi = int(yi-1)
                    newLocation = [[newYi, xi]]
                    self.change_location(newLocation)
        elif self.state == 1:
            if numGPS == 1:
                yi, xi = self.location[0]
                newYi = int(yi-1)
                newLocation = [[newYi, xi]]
                self.change_location(newLocation)

    def move_right(self):
        numGPS = len(self.location)
        if self.state == 2:
            # Nam dung
            if numGPS == 1:
                yi, xi = self.location[0]
                newXi1, newXi2 = int(xi+1), int(xi+2)
                newLocation = [[yi, newXi1],[yi, newXi2]]
                self.change_location(newLocation)
            else:
                # Nam ngang
                if self.is_horizontal():
                    yi, xi = self.location[1]
                    newXi = int(xi+1)
                    newLocation = [[yi, newXi]]
                    self.change_location(newLocation)
                # Nam Doc
                elif self.is_vertical():
                    y1, x1 = self.location[0]
                    y2, x2 = self.location[1]
                    newX1, newX2 = int(x1+1), int(x2+1)
                    newLocation = [[y1, newX1],[y2, newX2]]
                    self.change_location(newLocation)
        elif self.state == 1:
            if numGPS == 1:
                yi, xi = self.location[0]
                newXi = int(xi+1)
                newLocation = [[yi, newXi]]
                self.change_location(newLocation)

    def move_left(self):
        numGPS = len(self.location)
        if self.state == 2:
            # Nam dung
            if numGPS == 1:
                yi, xi = self.location[0]
                newXi1, newXi2 = int(xi-1), int(xi-2)
                newLocation = [[yi, newXi2],[yi, newXi1]]
                self.change_location(newLocation)
            else:
                # Nam ngang
                if self.is_horizontal():
                    yi, xi = self.location[0]
                    newXi = int(xi-1)
                    newLocation = [[yi, newXi]]
                    self.change_location(newLocation)
                # Nam Doc
                elif self.is_vertical():
                    y1, x1 = self.location[0]
                    y2, x2 = self.location[1]
                    newX1, newX2 = int(x1-1), int(x2-1)
                    newLocation = [[y1, newX1],[y2, newX2]]
                    self.change_location(newLocation)
        elif self.state == 1:
            if numGPS == 1:
                yi, xi = self.location[0]
                newXi = int(xi-1)
                newLocation = [[yi, newXi]]
                self.change_location(newLocation)

    def move_down(self):
        numGPS = len(self.location)
        if self.state == 2:
            # Nam dung
            if numGPS == 1:
                yi, xi = self.location[0]
                newYi1, newYi2 = int(yi+1), int(yi+2)
                newLocation = [[newYi2, xi],[newYi1, xi]]
                self.change_location(newLocation)
            else:
                # Nam ngang
                if self.is_horizontal():
                    y1, x1 = self.location[0]
                    y2, x2 = self.location[1]
                    newY1, newY2 = int(y1+1), int(y2+1)
                    newLocation = [[newY1, x1], [newY2, x2]]
                    self.change_location(newLocation)
                # Nam Doc
                elif self.is_vertical():
                    yi, xi = self.location[0]
                    newYi = int(yi+1)
                    newLocation = [[newYi, xi]]
                    self.change_location(newLocation)
        elif self.state == 1:
            if numGPS == 1:
                yi, xi = self.location[0]
                newYi = int(yi+1)
                newLocation = [[newYi, xi]]
                self.change_location(newLocation)
    
    def get_locaton(self):
        return self.location
    
    def check_verti_or_hori(self, location=None):
        if location != None:
            if len(location) == 2:
                y1, x1 = location[0]
                y2, x2 = location[1]
                if y1 == y2:
                    return Direction.horizontal
                if x1 == x2: 
                    return Direction.vertical
            else: return Direction.standing
        else:
            if len(self.location) == 2:
                y1, x1 = self.location[0]
                y2, x2 = self.location[1]
                if y1 == y2:
                    return Direction.horizontal
                if x1 == x2: 
                    return Direction.vertical
            else: return Direction.standing
            
    def change_location(self, location):
        self.pre_location = self.location
        self.location = location

    def on(self):
        self.active = True

    def off(self):
        self.active = False
    
    def is_horizontal(self):
        return self.check_verti_or_hori() == Direction.horizontal
    
    def is_vertical(self):
        return self.check_verti_or_hori() == Direction.vertical
    
    def is_standing(self):
        return len(self.location) == Direction.standing
            
    def is_singleBox(self):
        return self.state == 1
    
    def is_doubleBox(self):
        return self.state == 2