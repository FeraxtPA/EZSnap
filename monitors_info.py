import ctypes

user = ctypes.windll.user32


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

    def dump(self):
        return [int(val) for val in (self.left, self.top, self.right, self.bottom)]


class MONITORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_ulong),
        ("rcMonitor", RECT),
        ("rcWork", RECT),
        ("dwFlags", ctypes.c_ulong),
    ]


def get_monitors():
    monitors = []

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        monitor = MONITORINFO()
        monitor.cbSize = ctypes.sizeof(MONITORINFO)
        user.GetMonitorInfoA(hMonitor, ctypes.byref(monitor))
        monitors.append((hMonitor, monitor.rcMonitor))
        return True

    callback_func = ctypes.WINFUNCTYPE(
        ctypes.c_bool,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(RECT),
        ctypes.c_double,
    )
    user.EnumDisplayMonitors(None, None, callback_func(callback), 0)

    return monitors


def get_combined_monitor_size():
    monitors = get_monitors()
    leftmost = min(monitor.left for _, monitor in monitors)
    top = min(monitor.top for _, monitor in monitors)
    rightmost = max(monitor.right for _, monitor in monitors)
    bottom = max(monitor.bottom for _, monitor in monitors)
    return leftmost, top, rightmost, bottom
