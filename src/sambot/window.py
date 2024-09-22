import win32gui
import ctypes
from typing import Self
from PIL import ImageGrab, Image
from .window_math import Rect
from .controls import getCursorPos, setCursorPos
import math

ctypes.windll.user32.SetProcessDPIAware()
win32gui.GetForegroundWindow()

class Window:

    def __init__(self, handle: int):
        self.handle =handle


    #### Getters ####
    def name(self):
        return win32gui.GetWindowText(self.handle)

    def rect(self) -> Rect:
        return Rect.ofBox(win32gui.GetWindowRect(self.handle))


    #### Factory methods ####
    def get_foreground() -> Self:
        """ Get the currently focused window """
        return Window(win32gui.GetForegroundWindow())
    
    def get_desktop() -> Self:
        """ Get the desktop window """
        return Window(win32gui.GetDesktopWindow())
    
    def get_all() -> list[Self]:
        """ Get all the windows """
        def callback(handle, windows):
            windows.append(Window(handle))
            return True
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
    


    #### Utilities ####
    def screenshot(self, target: Rect=None) -> Image:
        """
        Take a screenshot of the window
        The optional parameter rect is the part of the window to screenshot, with the coordinates relative to the window width and height
        """

        desk= Window.get_desktop().rect()
        wind= self.rect()
        if(target is not None):
            assert 0 <= target.x <= 1
            assert 0 <= target.y <= 1
            assert 0 <= (target.x+target.width) <= 1
            assert 0 <= (target.y+target.height) <= 1
            wind.x= math.floor(wind.x*target.width)
            wind.y= math.floor(wind.y*target.height)
            wind.width= math.floor(wind.width*target.width)
            wind.height= math.floor(wind.height*target.height)

        
        x=wind.x
        y=wind.y
        width=wind.width
        height=wind.height

        offsetx=0
        offsety=0

        if wind.x<0:
            offsetx=-wind.x
            x=0
        
        if wind.y<0:
            offsety=-wind.y
            y=0

        if x+wind.width>desk.width:
            width=desk.width-x
        
        if y+wind.height>desk.height:
            height=desk.height-y

        screenshot= ImageGrab.grab(bbox=(x,y,x+width,y+height))
        total= Image.new(screenshot.mode, (wind.width, wind.height))
        total.paste(screenshot, (offsetx, offsety))
        return total
    
    def getRelativeCursorPos(self) -> tuple[float,float]:
        """ Get the cursor position relative to the window (between 0 and 1) """
        globalPos= getCursorPos()
        wind= self.rect()
        return ((globalPos.x-wind.left)/wind.width, (globalPos.y-wind.top)/wind.height)
    
    def setRelativeCursorPos(self, x:float, y:float):
        """ Set the cursor position relative to the window (between 0 and 1) """
        assert 0 <= x <= 1
        assert 0 <= y <= 1
        wind= self.rect()
        setCursorPos(int(wind.left()+wind.width*x), int(wind.top()+wind.height*y))


    def __str__(self):
        return f"Window: {self.title} ({self.width}x{self.height})"