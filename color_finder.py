import  win32api
import win32gui

mouse_pos = win32api.GetCursorPos()
while(True):

    if savedpos != win32api.GetCursorPos():
        mouse_pos = win32api.GetCursorPos()
        mouse_pos_x, mouse_pos_y = win32api.GetCursorPos()
        color = win32gui.GetPixel(win32gui.GetDC(None), mouse_pos_x, mouse_pos_y)
        red = color & 255
        green = (color >> 8) & 255
        blue = (color >> 16) & 255
        print("rgb(" + str(red) + "," + str(green) + "," + str(blue) + ")")
        print("moved to " + str(savedpos))
