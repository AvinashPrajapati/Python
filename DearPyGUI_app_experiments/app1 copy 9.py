import dearpygui.dearpygui as dpg
import os

dpg.create_context()
v = dpg.create_viewport(
    title="Custom Title",
    width=600,
    height=200,
    decorated=False,
    clear_color=(255, 255, 255, 255),
)

# Constants
MARGIN = 10
GRIP_SIZE = 25
MIN_WIDTH = 300
MIN_HEIGHT = 150

# Store drag state
resize_state = {
    "dragging": False,
    "start_mouse": (0, 0),
    "start_size": (0, 0),
}


class Cordinate:
    def __init__(self, p1=(0, 0), p2=(0, 0)):
        self.c1, self.c2 = (p1[0], p1[1]), (p2[0], p2[1])


def update_grip():
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()

    # Resize window and drawlist to match viewport
    dpg.set_item_width("Primary Window", w)
    dpg.set_item_height("Primary Window", h)
    dpg.set_item_width("main_drawlist", w)
    dpg.set_item_height("main_drawlist", h)

    # Move grip rectangle
    r1 = Cordinate(
        (w - GRIP_SIZE - MARGIN, h - GRIP_SIZE - MARGIN), (w - MARGIN, h - MARGIN)
    )
    dpg.configure_item("rect1", pmin=r1.c1, pmax=r1.c2)


# Is mouse in grip?
def is_mouse_in_grip():
    x, y = dpg.get_mouse_pos()
    x1, y1 = dpg.get_item_configuration("rect1")["pmin"]
    x2, y2 = dpg.get_item_configuration("rect1")["pmax"]
    return x1 <= x <= x2 and y1 <= y <= y2


# Start dragging
def start_drag():
    if is_mouse_in_grip():
        resize_state["dragging"] = True
        resize_state["start_mouse"] = dpg.get_mouse_pos()
        resize_state["start_size"] = (
            dpg.get_viewport_width(),
            dpg.get_viewport_height(),
        )


# Handle dragging
def handle_drag(_, __):
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


# End dragging
def stop_drag():
    resize_state["dragging"] = False


with dpg.window(
    tag="Primary Window",
    no_resize=False,
    no_move=False,
    width=dpg.get_viewport_width(),
    height=dpg.get_viewport_height(),
):
    dpg.add_button(label="x", callback=lambda: os._exit(0), pos=(10, 10))

    # Initial draw rectangle
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()
    dpg.draw_rectangle(
        tag="container",
        pmin=(0, 0),
        pmax=(w, h),
        fill=(0, 255, 0, 40),
    )
    r1 = Cordinate(
        (w - GRIP_SIZE - MARGIN, h - GRIP_SIZE - MARGIN), (w - MARGIN, h - MARGIN)
    )

    with dpg.drawlist(width=w, height=h, tag="main_drawlist"):
        dpg.draw_rectangle(
            tag="rect1",
            pmin=r1.c1,
            pmax=r1.c2,
            fill=(0, 0, 0, 255),
        )


# Mouse handlers
with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=lambda s, d: start_drag())
    dpg.add_mouse_drag_handler(callback=handle_drag)
    dpg.add_mouse_release_handler(callback=lambda s, d: stop_drag())


# Redraw grip on resize
dpg.set_viewport_resize_callback(lambda: update_grip())

dpg.setup_dearpygui()
dpg.show_viewport()
# update_grip()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()
