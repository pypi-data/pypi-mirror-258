from typing import Callable

from .constants import Constants
from .sysvars import SystemVariables
from .utils import remove_sketch


class BaseSketch(Constants, SystemVariables):
    id: str
    _p5js: object

    def __init__(self, id: str = "defaultCanvas0"):
        import js
        from pyodide.code import run_js

        self.id = id
        remove_sketch(self.id)
        create_sketch = f"var {self.id} = " + "new p5(() => { });"
        run_js(create_sketch)
        set_canvas_id = f"{self.id}.canvas.setAttribute('id', '{self.id}');"
        run_js(set_canvas_id)
        self._p5js = getattr(js.window, self.id)
        self._init_constants()
        self._update_system_variables()
    
    def run_sketch(
        self,
        preload: Callable | None = None,
        setup: Callable | None = None,
        draw: Callable | None = None,
        key_pressed: Callable | None = None,
        key_released: Callable | None = None,
        key_typed: Callable | None = None,
        mouse_moved: Callable | None = None,
        mouse_dragged: Callable | None = None,
        mouse_pressed: Callable | None = None,
        mouse_released: Callable | None = None,
        mouse_clicked: Callable | None = None,
        double_clicked: Callable | None = None,
        mouse_wheel: Callable | None = None,
        request_pointer_lock: Callable | None = None,
        exit_pointer_lock: Callable | None = None,
    ):
        """Runs a sketch in active mode."""
        import inspect
        from pyodide.ffi import create_proxy

        self._p5js._setupDone = False
        self._p5js._preloadDone = False
        self._p5js._millisStart = -1
        if callable(preload):
            self._p5js.preload = create_proxy(preload)
        if callable(setup):
            self._p5js.setup = create_proxy(setup)

        if callable(draw):

            def _draw(*args):
                self._update_system_variables()
                draw()

            self._p5js.draw = create_proxy(_draw)

        def wrap_event_func(func: Callable):
            args = inspect.signature(func).parameters
            if len(args) == 0:

                def wrapped_func(event):
                    func()

                return create_proxy(wrapped_func)
            else:
                return create_proxy(func)

        if callable(key_pressed):
            self._p5js.keyPressed = wrap_event_func(key_pressed)
        if callable(key_released):
            self._p5js.keyReleased = wrap_event_func(key_released)
        if callable(key_typed):
            self._p5js.keyTyped = wrap_event_func(key_typed)
        if callable(mouse_moved):
            self._p5js.mouseMoved = wrap_event_func(mouse_moved)
        if callable(mouse_dragged):
            self._p5js.mouseDragged = wrap_event_func(mouse_dragged)
        if callable(mouse_pressed):
            self._p5js.mousePressed = wrap_event_func(mouse_pressed)
        if callable(mouse_released):
            self._p5js.mouseReleased = wrap_event_func(mouse_released)
        if callable(mouse_clicked):
            self._p5js.mouseClicked = wrap_event_func(mouse_clicked)
        if callable(double_clicked):
            self._p5js.doubleClicked = wrap_event_func(double_clicked)
        if callable(mouse_wheel):
            self._p5js.mouseWheel = create_proxy(mouse_wheel)
        if callable(request_pointer_lock):
            self._p5js.requestPointerLock = create_proxy(request_pointer_lock)
        if callable(exit_pointer_lock):
            self._p5js.exitPointerLock = create_proxy(exit_pointer_lock)

        self._p5js._start()
