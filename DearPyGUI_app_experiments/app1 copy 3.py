import dearpygui.dearpygui as dpg
import os
from datetime import datetime, timedelta

# --- Config ---
WIDTH, HEIGHT = 475, 415
STRIP_HEIGHT = 40
dragging = {"active": False, "last": (0, 0)}


# --- Clock Update ---
def update_clock():
    now = datetime.now()
    dpg.set_value("current_time", now.strftime("%Y-%m-%d  %H:%M:%S"))

    midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    remaining = midnight - now
    dpg.set_value("countdown_time", str(remaining).split(".")[0])

    # Re-register for the next frame
    dpg.set_frame_callback(dpg.get_frame_count() + 1, update_clock)


# --- Drag Logic ---
def start_drag():
    mx, my = dpg.get_mouse_pos(local=False)
    if dpg.get_mouse_pos()[1] <= STRIP_HEIGHT:
        dragging["active"] = True
        dragging["last"] = (mx, my)


def stop_drag():
    dragging["active"] = False


def drag_window():
    if dragging["active"]:
        mx, my = dpg.get_mouse_pos(local=False)
        lx, ly = dragging["last"]
        dpg.set_viewport_pos(
            (
                dpg.get_viewport_pos()[0] + (mx - lx),
                dpg.get_viewport_pos()[1] + (my - ly),
            )
        )
        dragging["last"] = (mx, my)


# --- UI Setup ---
dpg.create_context()
dpg.create_viewport(
    title="Frameless Clock", width=WIDTH, height=HEIGHT, decorated=False
)

# Load a custom font if you have one, otherwise use default
font_tag = None
try:
    with dpg.font_registry():
        font_tag = dpg.add_font("C:\\Windows\\Fonts\\Arial.ttf", 124)
except Exception:
    font_tag = None  # Fallback to default

with dpg.window(
    tag="main",
    no_title_bar=True,
    no_resize=True,
    no_move=True,
    width=WIDTH,
    height=HEIGHT,
    on_close=lambda: os._exit(0),
):
    with dpg.drawlist(width=WIDTH, height=STRIP_HEIGHT):
        dpg.draw_rectangle(
            (0, 0), (WIDTH, STRIP_HEIGHT), fill=(50, 50, 80, 255), thickness=0
        )

    dpg.add_spacer(height=10)
    dpg.add_text("🕒 Current Time:", color=(200, 200, 200))
    dpg.add_text("", tag="current_time", color=(255, 255, 255))
    dpg.add_spacer(height=10)
    dpg.add_text("⏳ Time Left Today:", color=(200, 200, 200))
    dpg.add_text("", tag="countdown_time", color=(255, 255, 255))
    dpg.add_spacer(height=20)
    dpg.add_button(label="Exit", callback=lambda: dpg.stop_dearpygui())

# --- Handlers ---
with dpg.handler_registry():
    dpg.add_mouse_down_handler(callback=lambda s, d: start_drag())
    dpg.add_mouse_release_handler(callback=lambda s, d: stop_drag())
    dpg.add_mouse_drag_handler(callback=lambda s, d: drag_window(), threshold=0)

# --- Launch ---
dpg.setup_dearpygui()
if font_tag:
    dpg.bind_font(font_tag)
dpg.show_viewport()
dpg.set_primary_window("main", True)
dpg.set_frame_callback(dpg.get_frame_count() + 1, update_clock)
dpg.start_dearpygui()
dpg.destroy_context()
