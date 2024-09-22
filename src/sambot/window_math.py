



class Rect:
    """ Represent a rectangle """

    def __init__(self, x:int, y:int, width:int, height:int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def left(self):
        """ Get the x of the left side of the rectangle """
        return self.x
    
    def right(self):
        """ Get the x of the right side of the rectangle """
        return self.x + self.width
    
    def top(self):
        """ Get the y of the top side of the rectangle """
        return self.y
    
    def bottom(self):
        """ Get the y of the bottom side of the rectangle """
        return self.y + self.height

    def box(self):
        """ Get the box of the rectangle. (x of left, y of top, x of right, y of bottom) """
        return (self.x, self.y, self.x+self.width, self.y+self.height)

    def area(self):
        """ Get the area of the rectangle """
        return self.width * self.height

    def perimeter(self):
        """ Get the perimeter of the rectangle """
        return 2 * (self.width + self.height)
    
    def __str__(self):
        return f"Rect({self.x},{self.y},{self.width},{self.height})"

    def __iter__(self):
        return iter([self.x, self.y, self.width, self.height])


    #### Factory methods ####
    def ofBox(coordinates: tuple[int,int,int,int]):
        """ Create a rectangle from the given box coordinates """
        return Rect(coordinates[0], coordinates[1], coordinates[2]-coordinates[0], coordinates[3]-coordinates[1])