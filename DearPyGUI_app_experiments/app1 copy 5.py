import dearpygui.dearpygui as ui
import os
import time


class ui_settings:
    size = (475, 415)
    ui_dragging = False
    tabs = [
        "tab_1",
        # "tab_2",
        # "tab_3",
        "settings_tab",
    ]


class scaling:
    section_width = ui_settings.size[0] - 20
    section_height = ui_settings.size[1] - 75
    button_size = (115, 25)
    spacing_offset = 10


ui.create_context()

viewport = ui.create_viewport(
    title="window_title",
    width=ui_settings.size[0],
    height=ui_settings.size[1],
    decorated=False,
    resizable=True,  # <-- Enable resizing
    max_width=475,
    max_height=415,
)

ui.setup_dearpygui()

with ui.window(
    label="example",
    tag="main",
    width=ui_settings.size[0],
    height=ui_settings.size[1],
    no_collapse=True,
    no_move=True,
    no_resize=False,
    on_close=lambda: os._exit(0),
) as win:
    ui.add_text("Resize viewport to test background sync")
    ui.add_input_text()


# --- Resize callback to sync window size with viewport ---
def resize_viewport_callback():
    width = ui.get_viewport_width()
    height = ui.get_viewport_height()
    ui.set_item_width("main", width)
    ui.set_item_height("main", height)


ui.set_viewport_resize_callback(resize_viewport_callback)


# --- Drag logic ---
def is_dragging(_, data):
    if ui.is_mouse_button_down(0):
        y = data[1]
        if -2 <= y <= 19:
            ui_settings.ui_dragging = True
    else:
        ui_settings.ui_dragging = False


def drag_logic(_, data):
    if ui_settings.ui_dragging:
        pos = ui.get_viewport_pos()
        dx = data[1]
        dy = data[2]
        ui.configure_viewport(viewport, x_pos=pos[0] + dx, y_pos=pos[1] + dy)


with ui.handler_registry():
    ui.add_mouse_drag_handler(0, callback=drag_logic)
    ui.add_mouse_move_handler(callback=is_dragging)

ui.set_primary_window("main", True)
ui.show_viewport()
ui.start_dearpygui()
ui.destroy_context()
