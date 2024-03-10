from functools import partial
import time
import datetime
from PIL import ImageGrab, Image
from io import BytesIO
import win32clipboard
import pygetwindow as gw
import os


def map_to_virtual_canvas(
    x,
    y,
    leftmost,
    top,
):
    return x + leftmost, y + top


def activate_select_window_mode(root, canvas, leftmost, top, rightmost, is_selected):
    root.bind(
        "<Motion>",
        lambda event: draw_rectangle_on_window(
            event, root, canvas, leftmost, top, rightmost
        ),
    )
    root.bind(
        "<Button-1>", lambda event: take_window_screenshot(event, root, is_selected)
    )


def draw_rectangle(
    canvas,
    start_x,
    start_y,
    end_x,
    end_y,
):
    canvas.delete("rectangle")  # Clear previous rectangle
    canvas.create_rectangle(
        start_x,
        start_y,
        end_x,
        end_y,
        outline="white",
        tags="rectangle",
        fill="#808080",
        width=3,
    )


def capture_screenshot(x1, y1, x2, y2):
    # Ensure x2 and y2 are greater than x1 and y1
    x1, x2 = min(x1, x2), max(x1, x2)
    y1, y2 = min(y1, y2), max(y1, y2)

    current_datetime = datetime.datetime.now()
    filename = current_datetime.strftime("%d.%m.%Y_%H%M%S") + ".png"

    user_name = os.getlogin()

    path = f"C:\\Users\\{user_name}\\Pictures\\EZSnaps"

    if not os.path.exists(path):
        os.makedirs(path)

    full_path = os.path.join(path, filename)

    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2), all_screens=True)
    screenshot.save(full_path)

    image = Image.open(full_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)


def take_window_screenshot(event, root, is_selected):
    if is_selected:
        is_selected = False

        root.withdraw()
        time.sleep(0.01)

        # Get cursor position
        x, y = event.x_root, event.y_root

        window = gw.getWindowsAt(x, y)

        window = window[0]

        x1, y1, x2, y2 = window.left, window.top, window.right, window.bottom

        if window:
            capture_screenshot(x1 + 8, y1, x2 - 8, y2 - 8)

        else:
            is_selected = False
            pass


def draw_rectangle_on_window(event, root, canvas, leftmost, top, rightmost):
    x, y = event.x_root, event.y_root

    window = gw.getWindowsAt(x, y)

    # Filter out canvas window
    tk_window_title = root.title()
    window = [win for win in window if win.title != tk_window_title]
    window = window[0]

    if window:
        canvas.delete("window_rect")
        if window.left < -10:
            canvas.create_rectangle(
                window.left - leftmost,
                window.top,
                window.right - leftmost,
                window.bottom,
                outline="white",
                tags="window_rect",
                fill="#808080",
                width=2,
            )
        elif window.left > -15:
            canvas.create_rectangle(
                -leftmost + window.left,
                window.top,
                window.right - leftmost,
                window.bottom,
                outline="white",
                tags="window_rect",
                fill="#808080",
                width=2,
            )
        else:
            pass


def send_to_clipboard(clip_type, data):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()


def take_fullscreen_screenshot(root):
    root.destroy()
    time.sleep(0.01)
    ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)
    screenshot = ImageGrab.grab()
    current_datetime = datetime.datetime.now()
    filename = current_datetime.strftime("%d.%m.%Y_%H-%M-%S") + ".png"

    user_name = os.getlogin()

    path = f"C:\\Users\\{user_name}\\Pictures\\EZSnaps"

    if not os.path.exists(path):
        os.makedirs(path)

    full_path = os.path.join(path, filename)
    screenshot.save(full_path)

    image = Image.open(full_path)
    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()
    send_to_clipboard(win32clipboard.CF_DIB, data)
