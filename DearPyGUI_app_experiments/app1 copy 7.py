import dearpygui.dearpygui as dpg
import os

# Setup
dpg.create_context()
v = dpg.create_viewport(
    title="Resizable Window", decorated=False, width=300, height=300
)
dpg.setup_dearpygui()

resizing = {"active": False}
resize_margin = 8
resize_box_size = 15

# UI
with dpg.window(tag="MainWindow", no_move=True, no_resize=True, no_scrollbar=True):
    dpg.add_text("Drag bottom-right box to resize")
    dpg.add_button(
        label="x", tag="exit_button", width=30, height=30, callback=lambda: os._exit(0)
    )
    with dpg.drawlist(width=0, height=0, tag="resize_drawlist"):
        pass


# Utility to update draw elements
def update_draw_elements():
    w = dpg.get_viewport_width()
    h = dpg.get_viewport_height()

    dpg.set_item_width("resize_drawlist", w)
    dpg.set_item_height("resize_drawlist", h)

    dpg.set_item_pos("exit_button", [w - 40, 10])

    dpg.delete_item("resize_drawlist", children_only=True)
    dpg.draw_rectangle(
        pmin=(w - 200, h - 200),
        pmax=(w - 100, h - 100),
        color=(255, 255, 255, 255),
        # fill=(255, 255, 255, 100),
        parent="resize_drawlist",
    )


# Logic: Detect if mouse is over resize box
def is_mouse_in_resize_box(x, y):
    w = dpg.get_viewport_width()
    h = dpg.get_viewport_height()
    x1 = w - resize_box_size - resize_margin
    y1 = h - resize_box_size - resize_margin
    x2 = w - resize_margin
    y2 = h - resize_margin
    return x1 <= x <= x2 and y1 <= y <= y2


# Global to store drag start info
drag_start = {"x": 0, "y": 0, "w": 0, "h": 0}


def on_mouse_move(_, data):
    x, y = data
    if (
        dpg.is_mouse_button_down(0)
        and is_mouse_in_resize_box(x, y)
        and not resizing["active"]
    ):

        resizing["active"] = True
        drag_start["x"] = x
        drag_start["y"] = y
        drag_start["w"] = dpg.get_viewport_width()
        drag_start["h"] = dpg.get_viewport_height()
        print(f"Start Resize At: {x}, {y}")
    elif not dpg.is_mouse_button_down(0):
        resizing["active"] = False


def on_mouse_drag(_, data):
    x, y = dpg.get_mouse_pos()
    if resizing["active"]:
        dx = x - drag_start["x"]
        dy = y - drag_start["y"]
        new_width = max(300, drag_start["w"] + dx)
        new_height = max(200, drag_start["h"] + dy)
        dpg.configure_viewport(v, width=new_width, height=new_height)
        update_draw_elements()


# Register handlers
with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=on_mouse_move)
    dpg.add_mouse_drag_handler(button=0, callback=on_mouse_drag)

# Viewport show
dpg.set_viewport_resize_callback(lambda: update_draw_elements())
dpg.show_viewport()
# update_draw_elements()
dpg.set_primary_window("MainWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
