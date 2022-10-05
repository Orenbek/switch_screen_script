from AppKit import NSScreen
from Quartz.CoreGraphics import CGEventCreateMouseEvent, CGEventPost, kCGEventMouseMoved, CGEventCreate, CGEventGetLocation
from Quartz.CoreGraphics import kCGEventLeftMouseDown, kCGEventLeftMouseUp, kCGMouseButtonLeft, kCGHIDEventTap


def mouseEvent(type, posx, posy):
    theEvent = CGEventCreateMouseEvent(
        None,
        type,
        (posx, posy),
        kCGMouseButtonLeft)
    CGEventPost(kCGHIDEventTap, theEvent)


def mouse_move(posx, posy):
    mouseEvent(kCGEventMouseMoved, posx, posy)


def mouse_click(posx, posy):
    # uncomment this line if you want to force the mouse
    # to MOVE to the click location first (I found it was not necessary).
    #mouseEvent(kCGEventMouseMoved, posx,posy);
    mouseEvent(kCGEventLeftMouseDown, posx, posy)
    mouseEvent(kCGEventLeftMouseUp, posx, posy)


def get_main_screen_frame():
    return NSScreen.screens()[0].frame()


def get_screen_mouse_range(screen_frame):
    main_screen_height = get_main_screen_frame().size.height
    origin = screen_frame.origin
    size = screen_frame.size
    return {
        "lt": (origin.x, main_screen_height - origin.y - size.height),
        "lb": (origin.x, main_screen_height - origin.y),
        "rt": (origin.x + size.width, main_screen_height - origin.y - size.height),
        "rb": (origin.x + size.width, main_screen_height - origin.y)
    }


def move_mouse_to_center(screen_frame):
    (ltx, lty) = get_screen_mouse_range(screen_frame)["lt"]
    mouse_click(ltx + screen_frame.size.width / 2,
                lty + screen_frame.size.height / 2)


def get_mouse_location():
    event = CGEventCreate(None)
    loc = CGEventGetLocation(event)
    return loc


def main():
    loc = get_mouse_location()
    for screen in NSScreen.screens():
        mouse_range = get_screen_mouse_range(screen.frame())
        if (loc.x < mouse_range["lt"][0] or loc.x > mouse_range["rb"][0]) or loc.y < mouse_range["lt"][1] or loc.y > mouse_range["rb"][1]:
            move_mouse_to_center(screen.frame())


__name__ == '__main__' and main()
