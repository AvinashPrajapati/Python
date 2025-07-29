import dearpygui.dearpygui as dpg

dpg.create_context()
dpg.create_viewport(title="Rectangle Interaction Test", width=500, height=400)
dpg.setup_dearpygui()

# Define multiple rectangles with unique tags and bounding boxes
rectangles = {
    "rect1": {"pmin": (50, 50), "pmax": (150, 120)},
    "rect2": {"pmin": (200, 80), "pmax": (300, 150)},
    "rect3": {"pmin": (100, 200), "pmax": (250, 280)},
}

# Create drawlist and draw rectangles
with dpg.window(tag="MainWindow"):
    with dpg.drawlist(width=500, height=400, tag="main_drawlist"):
        for tag, rect in rectangles.items():
            dpg.draw_rectangle(
                pmin=rect["pmin"],
                pmax=rect["pmax"],
                color=(255, 255, 255, 255),
                fill=(100, 100, 255, 100),
                tag=tag,
            )


# Utility: Hit-test mouse against rectangle bounds
def get_rect_under_mouse():
    x, y = dpg.get_mouse_pos()
    for tag, rect in rectangles.items():
        x1, y1 = rect["pmin"]
        x2, y2 = rect["pmax"]
        if x1 <= x <= x2 and y1 <= y <= y2:
            return tag
    return None


# Track state
mouse_state = {
    "hovering": None,
    "pressing": None,
    "dragging": None,
}


# Mouse move = hovering
def on_mouse_move(_, data):
    tag = get_rect_under_mouse()
    if tag != mouse_state["hovering"]:
        mouse_state["hovering"] = tag
        if tag:
            print(f"Hovering over: {tag}")
        else:
            print("Not hovering over any rectangle")


# Mouse down = pressing
def on_mouse_down():
    tag = get_rect_under_mouse()
    mouse_state["pressing"] = tag
    if tag:
        print(f"Mouse down inside: {tag}")


# Mouse drag = dragging
def on_mouse_drag(_, data):
    if mouse_state["pressing"]:
        tag = get_rect_under_mouse()
        if tag and tag != mouse_state["dragging"]:
            mouse_state["dragging"] = tag
            print(f"Dragging inside: {tag}")
        elif not tag and mouse_state["dragging"]:
            print(f"Dragged out of {mouse_state['dragging']}")
            mouse_state["dragging"] = None


# Mouse up = reset
def on_mouse_up():
    if mouse_state["pressing"]:
        print(f"Mouse released (was pressing): {mouse_state['pressing']}")
        mouse_state["pressing"] = None
        mouse_state["dragging"] = None


# Handler setup
with dpg.handler_registry():
    dpg.add_mouse_move_handler(callback=on_mouse_move)
    dpg.add_mouse_click_handler(callback=lambda s, a: on_mouse_down())
    dpg.add_mouse_drag_handler(0, callback=on_mouse_drag)
    dpg.add_mouse_release_handler(callback=lambda: on_mouse_up())

# Show viewport
dpg.show_viewport()
dpg.set_primary_window("MainWindow", True)
dpg.start_dearpygui()
dpg.destroy_context()
