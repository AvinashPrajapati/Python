import dearpygui.dearpygui as ui
import os


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
    resizable=True,
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
    no_resize=True,
    on_close=lambda: os._exit(0),
) as win:
    ui.add_input_text()


def lerp(a, b, t):
    return a + (b - a) * t


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
        x = data[1]
        y = data[2]

        current_spacing_offset = pos[0]
        current_y = pos[1]

        speed = float(0.1)
        interpolated_x = lerp(current_spacing_offset, pos[0] + x, speed)
        interpolated_y = lerp(current_y, pos[1] + y, speed)

        ui.configure_viewport(viewport, x_pos=interpolated_x, y_pos=interpolated_y)


with ui.handler_registry():
    ui.add_mouse_drag_handler(0, callback=drag_logic)
    ui.add_mouse_move_handler(callback=is_dragging)

ui.show_viewport()
ui.start_dearpygui()
ui.destroy_context()
