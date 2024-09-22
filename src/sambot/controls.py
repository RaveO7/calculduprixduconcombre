import win32api
import win32con
import win32com
import enum

class Key(enum.Enum):
    A= ord("a")
    B= A+1
    C= A+2
    D= A+3
    E= A+4
    F= A+5
    G= A+6
    H= A+7
    I= A+8
    J= A+9
    K= A+10
    L= A+11
    M= A+12
    N= A+13
    O= A+14
    P= A+15
    Q= A+16
    R= A+17
    S= A+18
    T= A+19
    U= A+20
    V= A+21
    W= A+22
    X= A+23
    Y= A+24
    Z= A+25
    SPACE= win32con.VK_SPACE
    ENTER= win32con.VK_RETURN
    ESC= win32con.VK_ESCAPE
    TAB= win32con.VK_TAB
    SHIFT= win32con.VK_SHIFT
    CTRL= win32con.VK_CONTROL
    ALT= win32con.VK_MENU
    BACKSPACE= win32con.VK_BACK
    CAPSLOCK= win32con.VK_CAPITAL
    F1= win32con.VK_F1
    F2= win32con.VK_F2
    F3= win32con.VK_F3
    F4= win32con.VK_F4
    F5= win32con.VK_F5
    F6= win32con.VK_F6
    F7= win32con.VK_F7
    F8= win32con.VK_F8
    F9= win32con.VK_F9
    F10= win32con.VK_F10
    F11= win32con.VK_F11
    F12= win32con.VK_F12
    UP= win32con.VK_UP
    DOWN= win32con.VK_DOWN
    LEFT= win32con.VK_LEFT
    RIGHT= win32con.VK_RIGHT
    NUM0= win32con.VK_NUMPAD0
    NUM1= win32con.VK_NUMPAD1
    NUM2= win32con.VK_NUMPAD2
    NUM3= win32con.VK_NUMPAD3
    NUM4= win32con.VK_NUMPAD4
    NUM5= win32con.VK_NUMPAD5
    NUM6= win32con.VK_NUMPAD6
    NUM7= win32con.VK_NUMPAD7
    NUM8= win32con.VK_NUMPAD8
    NUM9= win32con.VK_NUMPAD9
    NUMLOCK= win32con.VK_NUMLOCK
    SCROLLLOCK= win32con.VK_SCROLL
    INSERT= win32con.VK_INSERT
    DELETE= win32con.VK_DELETE
    HOME= win32con.VK_HOME
    END= win32con.VK_END
    PAGEUP= win32con.VK_PRIOR
    PAGEDOWN= win32con.VK_NEXT
    PRINTSCREEN= win32con.VK_SNAPSHOT
    PAUSE= win32con.VK_PAUSE
    WIN= win32con.VK_LWIN
    RWIN= win32con.VK_RWIN
    APPS= win32con.VK_APPS
    MEDIA_NEXT= win32con.VK_MEDIA_NEXT_TRACK
    MEDIA_PREV= win32con.VK_MEDIA_PREV_TRACK
    MEDIA_PLAY= win32con.VK_MEDIA_PLAY_PAUSE
    VOLUME_MUTE= win32con.VK_VOLUME_MUTE
    VOLUME_DOWN= win32con.VK_VOLUME_DOWN
    VOLUME_UP= win32con.VK_VOLUME_UP
    MOUSE_LEFT= win32con.VK_LBUTTON
    MOUSE_RIGHT= win32con.VK_RBUTTON
    MOUSE_MIDDLE= win32con.VK_MBUTTON
    MOUSE_X1= win32con.VK_XBUTTON1
    MOUSE_X2= win32con.VK_XBUTTON2

    def isPressed(self):
        return isKeyPressed(self)
    
    def press(self):
        pressKey(self)

    def release(self):
        releaseKey(self)

def isKeyPressed(key: Key):
    """
    Check if the given key is pressed. Work for both keyboard and mouse buttons.
    """
    return win32api.GetAsyncKeyState(key.value)<0

def pressKey(key: Key):
    """
    Press the given key. Work for both keyboard and mouse buttons.
    """
    win32api.keybd_event(key.value, 0, 0)

def releaseKey(key: Key):
    """
    Release the given key. Work for both keyboard and mouse buttons.
    """
    win32api.keybd_event(key.value, 0, 2)


def getCursorPos() -> tuple[int,int]:
    """
    Get the current cursor position
    - returns : a tuple of the x and y coordinates of the cursor in pixel
    """
    return win32api.GetCursorPos()

def setCursorPos(x:int, y:int):
    """
    Set the cursor position
    - x : the x coordinate of the cursor in pixel
    - y : the y coordinate of the cursor in pixel
    """
    win32api.SetCursorPos((x,y))
