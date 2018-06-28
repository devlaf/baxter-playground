from robot_utils import Side
from baxter_interface import DigitalIO

class BaxterButton(object):

    def __init__(self, digital_io_str):
        DigitalIO(digital_io_str).state_changed.connect(self.state_change)
        self._on_pressed_funcs = []
        self._on_released_funcs = []

    def register_on_pressed_handler(self, func):
        self._on_pressed_funcs.append(func)

    def register_on_released_handler(self, func):
        self._on_released_funcs.append(func)

    def state_change(self, value):
        if value == True:
            for func in self._on_pressed_funcs:
                func()
        else:
            for func in self._on_released_funcs:
                func()
