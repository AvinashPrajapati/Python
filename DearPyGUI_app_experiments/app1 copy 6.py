import dearpygui.dearpygui as ui
import os
import time


class ui_settings:
    size = (400, 415)
    ui_dragging = False


def config_size(size=ui_settings.size, padding=5):
    return [size[0] - (2 * padding) + 3, size[0] - (2 * padding)]


ui.create_context()

viewport = ui.create_viewport(
    title="window_title",
    width=ui_settings.size[0],
    height=ui_settings.size[1],
    decorated=False,
    resizable=True,  # <-- Enable resizing
    always_on_top=True,
)

ui.setup_dearpygui()

with ui.window(
    label="example",
    tag="main",
    # width=ui_settings.size[0],
    # height=ui_settings.size[1],
    no_collapse=True,
    no_move=True,
    no_resize=False,
    on_close=lambda: os._exit(0),
    # min_size=[400, 400],
) as win:
    size = config_size(padding=10)
    ui.draw_rectangle(
        label="Resize viewport to test background sync",
        before="ramesh",
        parent="main",
        tag="titlebar",
        pmin=(-6, -6),
        pmax=(size[0] + 8, size[1] + 25),
        fill=(0, 0, 0, 0),
    )

    ui.add_button(label="x", callback=lambda: os._exit(0))


# --- Drag logic ---
def is_dragging(_, data):
    if ui.is_mouse_button_down(0):
        x = data[0]
        y = data[1]
        if (
            (15 <= y <= 25) and (80 < x < (ui_settings.size[0] - 5))
        ) and ui.is_mouse_button_down(0):
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
    # resize

ui.set_primary_window("main", True)
ui.show_viewport()
ui.start_dearpygui()
ui.destroy_context()
