import dearpygui.dearpygui as dpg
import os

dpg.create_context()
dpg.create_viewport(
    title="Frameless with Top Strip", width=640, height=400, decorated=False
)
dpg.setup_dearpygui()

WIDTH, HEIGHT = 640, 400
STRIP_HEIGHT = 40
STRIP_COLOR = (50, 50, 80, 255)  # dark blue-ish RGBA

# Main window without titlebar
with dpg.window(
    tag="Main",
    no_title_bar=True,
    no_resize=True,
    no_move=True,
    no_background=False,
    width=WIDTH,
    height=HEIGHT,
):

    # This will draw on top of the window itself
    with dpg.drawlist(width=WIDTH, height=HEIGHT):
        dpg.draw_rectangle(
            pmin=(0, 0),
            pmax=(WIDTH, STRIP_HEIGHT),
            color=STRIP_COLOR,
            fill=STRIP_COLOR,
            thickness=0,
        )

    dpg.add_spacing(count=4)
    dpg.add_text("This is a custom title strip")
    dpg.add_button(label="Exit", callback=lambda: dpg.stop_dearpygui())

dpg.show_viewport()
dpg.set_primary_window("Main", True)
dpg.start_dearpygui()
dpg.destroy_context()
