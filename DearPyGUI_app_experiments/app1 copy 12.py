import dearpygui.dearpygui as dpg
import os

# Constants
MARGIN = 9
GRIP_SIZE = 10
MIN_WIDTH = 300
MIN_HEIGHT = 150

WINDOW_SIZE = [600, 300]

# Store drag state
resize_state = {
    "titlebar_drag": False,
    "dragging": False,
    "start_mouse": (0, 0),
    "start_size": (0, 0),
}


class Cordinate:
    def __init__(self, p1=(0, 0), p2=(0, 0)):
        self.c1, self.c2 = (p1[0], p1[1]), (p2[0], p2[1])


dpg.create_context()


v = dpg.create_viewport(
    title="Custom Title",
    width=WINDOW_SIZE[0],
    height=WINDOW_SIZE[1],
    decorated=False,
    always_on_top=True,
)


with dpg.window(
    tag="Primary Window",
):
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()
    dpg.add_button(
        tag="close_window",
        label="x",
        callback=lambda: os._exit(0),
        pos=(dpg.get_viewport_width() - MARGIN - GRIP_SIZE - 5, 5),
    )

    # Resizing widget
    dpg.add_text("Application", parent="rect3")

    p1 = (w - GRIP_SIZE - MARGIN, h - GRIP_SIZE - MARGIN)
    p2 = (w - MARGIN, h - MARGIN)
    r1 = Cordinate(p1=p1, p2=p2)
    dpg.draw_rectangle(
        tag="rect1",
        pmin=r1.c1,
        pmax=r1.c2,
        fill=(0, 0, 0, 255),
    )
    # Write main widget
    dpg.draw_line(
        tag="title_bar_divider",
        p1=(0 - MARGIN, 25),
        p2=(dpg.get_viewport_width() - MARGIN, 25),
        color=(255, 255, 255, 100),
    )
    dpg.add_spacer(height=5)
    with dpg.child_window(label="Tutorial", tag="main", border=True):

        dpg.add_button(label="Button 1", callback=lambda: os._exit(0))
        dpg.add_button(label="Button 2")


def update_grip():
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()

    # Resize window and drawlist to match viewport
    dpg.set_item_width("Primary Window", w)
    dpg.set_item_height("Primary Window", h)

    # Move grip rectangle
    p1 = (w - GRIP_SIZE - MARGIN, h - GRIP_SIZE - MARGIN)
    p2 = (w - MARGIN, h - MARGIN)
    r1 = Cordinate(p1, p2)
    dpg.configure_item("rect1", pmin=r1.c1, pmax=r1.c2)

    # update close
    dpg.configure_item("close_window", pos=(p1[0], 5))
    dpg.configure_item("title_bar_divider", p2=(p2[0], 25))


# Is mouse in grip?
def is_mouse_in_titlebar():
    mx, my = dpg.get_mouse_pos()
    c1 = -20 <= my <= 13
    c2 = 0 < mx < dpg.get_viewport_width() - (MARGIN + GRIP_SIZE + 10)
    return c1 and c2


# Is mouse in grip?
def is_mouse_in_grip():
    mx, my = dpg.get_mouse_pos()
    x1, y1 = dpg.get_item_configuration("rect1")["pmin"]
    x2, y2 = dpg.get_item_configuration("rect1")["pmax"]
    cx = x1 + MARGIN - 1 < mx < x2 + MARGIN + 1
    cy = y1 - GRIP_SIZE - 1 < my < y2 - GRIP_SIZE + 1
    return cx and cy


# Start dragging
def start_drag():
    if is_mouse_in_grip():
        resize_state["dragging"] = True
        resize_state["start_mouse"] = dpg.get_mouse_pos()
        resize_state["start_size"] = (
            dpg.get_viewport_width(),
            dpg.get_viewport_height(),
        )
    if is_mouse_in_titlebar():
        resize_state["titlebar_drag"] = True


# Handle dragging
def handle_drag(_, data):
    if resize_state["dragging"]:
        x, y = dpg.get_mouse_pos()
        sx, sy = resize_state["start_mouse"]
        dx = x - sx
        dy = y - sy
        w0, h0 = resize_state["start_size"]
        new_w = max(MIN_WIDTH, int(w0 + dx))
        new_h = max(MIN_HEIGHT, int(h0 + dy))
        dpg.configure_viewport(v, width=new_w, height=new_h)
        update_grip()
    if resize_state["titlebar_drag"]:
        pos = dpg.get_viewport_pos()
        dx = data[1]
        dy = data[2]
        dpg.configure_viewport(v, x_pos=pos[0] + dx, y_pos=pos[1] + dy)


# End dragging
def stop_drag():
    resize_state["dragging"] = False
    resize_state["titlebar_drag"] = False


# Mouse handlers
with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=start_drag)
    dpg.add_mouse_drag_handler(callback=handle_drag)
    # dpg.add_mouse_move_handler(callback=is_dragging)
    dpg.add_mouse_release_handler(callback=stop_drag)


# Redraw grip on resize
dpg.set_viewport_resize_callback(lambda: update_grip())

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
