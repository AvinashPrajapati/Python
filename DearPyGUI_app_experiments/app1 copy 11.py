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
MARGIN = 9
GRIP_SIZE = 10
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


with dpg.window(
    tag="Primary Window",
    width=dpg.get_viewport_width(),
    height=dpg.get_viewport_height(),
    no_title_bar=False,
):
    w, h = dpg.get_viewport_width(), dpg.get_viewport_height()

    dpg.add_button(
        label="x",
        callback=lambda: os._exit(0),
        pos=(dpg.get_viewport_width() - MARGIN - GRIP_SIZE - 5, 5),
    )

    # Resizing widget
    dpg.add_text("Application", parent="rect3")

    r1 = Cordinate(
        (w - GRIP_SIZE - MARGIN, h - GRIP_SIZE - MARGIN), (w - MARGIN, h - MARGIN)
    )
    dpg.draw_rectangle(
        tag="rect1",
        pmin=r1.c1,
        pmax=r1.c2,
        fill=(0, 0, 0, 255),
    )
    # Write main widget
    dpg.draw_line(
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
    r1 = Cordinate(
        (w - GRIP_SIZE - MARGIN, h - GRIP_SIZE - MARGIN), (w - MARGIN, h - MARGIN)
    )
    dpg.configure_item("rect1", pmin=r1.c1, pmax=r1.c2)


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

        # w, h = dpg.get_viewport_width(), dpg.get_viewport_height()
        # dpg.configure_item(
        #     "rect2",
        #     pmin=(0 - MARGIN + 2, 0 - MARGIN + 2),
        #     pmax=(w - MARGIN, h - MARGIN),
        # )


# End dragging
def stop_drag():
    resize_state["dragging"] = False


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
