import time
import keyboard
from tkinter import Tk, Canvas, Button, PhotoImage, Frame
from monitors_info import get_combined_monitor_size
from screenshot import (
    draw_rectangle,
    map_to_virtual_canvas,
    capture_screenshot,
    take_fullscreen_screenshot,
    activate_select_window_mode,
)
from screeninfo import get_monitors

class ScreenshotTool:
    def __init__(self):
        self.root = None
        self.canvas = None
        self.width = None
        self.leftmost = None
        self.top = None
        self.rightmost = None
        self.start_x = 0
        self.start_y = 0
        self.selecting = False

    def create_canvas(self):
        self.leftmost, self.top, self.rightmost, bottom = get_combined_monitor_size()
        self.width = self.rightmost - self.leftmost

        self.root = Tk()
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.4)
        self.root.geometry(f"{self.width}x{bottom - self.top}+{self.leftmost}+{self.top}")
        self.root.overrideredirect(True)

        self.canvas = Canvas(self.root, bg="black", highlightthickness=0, cursor="cross")
        self.canvas.pack(fill="both", expand=True)

    def on_press(self, event):
        self.start_x, self.start_y = event.x, event.y

    def on_drag(self, event):
        end_x, end_y = event.x, event.y
        draw_rectangle(self.canvas, self.start_x, self.start_y, end_x, end_y)
        self.selecting = True

    def on_release(self, event):
        self.root.destroy()

        if self.selecting and abs(event.x - self.start_x) > 10 and abs(event.y - self.start_y) > 10:
            abs_start_x, abs_start_y = map_to_virtual_canvas(self.start_x, self.start_y, self.leftmost, self.top)
            abs_end_x, abs_end_y = map_to_virtual_canvas(event.x, event.y, self.leftmost, self.top)
              
            capture_screenshot(abs_start_x, abs_start_y, abs_end_x, abs_end_y)
        self.selecting = False

    def exit_(self, event):
        self.root.destroy()

    def main(self):
        for m in get_monitors():
            if m.is_primary:
                main_monitor_width = m.width

        while True:
            if keyboard.is_pressed("f10"):
                self.create_canvas()

                self.canvas.bind("<Button-1>", self.on_press)
                self.canvas.bind("<B1-Motion>", self.on_drag)
                self.canvas.bind("<ButtonRelease-1>", self.on_release)
                self.canvas.bind("<ButtonRelease-3>", self.exit_)

                widget_frame_width = 64
                widget_frame = Frame(self.canvas, height=48, width=widget_frame_width, bg="white", padx=2, pady=2)
                  
                fullscreen_image = PhotoImage(file="assets/fullscreen.png")
                fullscreen_button = Button(
                    widget_frame,
                    command=lambda: take_fullscreen_screenshot(self.root),
                    image=fullscreen_image,
                    bg="black",
                    bd=0,
                    height=24,
                    width=24,
                )
                fullscreen_button.pack(side="left", ipadx=5, anchor="center", ipady=5)

                select_window_image = PhotoImage(file="assets/window.png")
                select_window_button = Button(
                    widget_frame,
                    command=lambda: activate_select_window_mode(self.root, self.canvas, self.leftmost, self.top, self.rightmost, is_selected=True),
                    image=select_window_image,
                    bg="black",
                    bd=0,
                )
                select_window_button.pack(side="left", ipadx=5, anchor="center", ipady=5)

                if self.leftmost < 0:
                    frame_pos = self.width - (main_monitor_width / 2) - (widget_frame_width / 2)
                elif self.rightmost > 3860:
                    frame_pos = (main_monitor_width / 2) - (widget_frame_width / 2)
                elif self.leftmost < 0 and self.rightmost > 3860:
                    frame_pos = (self.width / 2) - (widget_frame_width / 2)

                widget_frame.place(x=frame_pos, rely=0.02)

                self.root.mainloop()
            else:
                time.sleep(0.01)

if __name__ == "__main__":
    screenshot_tool = ScreenshotTool()
    screenshot_tool.main()
