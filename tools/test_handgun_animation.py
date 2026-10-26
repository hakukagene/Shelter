"""Validate uploaded frames and exercise sandbox state transitions without a GPU."""
from pathlib import Path
from types import SimpleNamespace
import textwrap
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "game/shooting_test.rpy").read_text()
code = textwrap.dedent(source.split("init python:\n", 1)[1].split("\nstyle ", 1)[0])
code = code.replace("import pygame", "# pygame supplied by test")
clock = [0.0]
noop = lambda *args, **kwargs: None
renpy = SimpleNamespace(Displayable=object, displayable=lambda path: path,
    get_game_runtime=lambda: clock[0], redraw=noop,
    music=SimpleNamespace(register_channel=noop, play=noop))
scope = {"renpy": renpy, "pygame": SimpleNamespace()}
exec(compile(code, "shooting_test.rpy", "exec"), scope)
for index in range(20):
    with Image.open(ROOT / ("game/images/shooting_test/frames/handgun-%02d.png" % index)) as frame:
        assert frame.mode == "RGBA"
        assert frame.height == 360 and frame.width in (204, 205)
        assert frame.getchannel("A").getextrema()[0] == 0
for name in ("SHOOTING_TEST_FIRE_SEQUENCE", "SHOOTING_TEST_RELOAD_SEQUENCE"):
    sequence = scope[name]
    assert all(0 <= frame < 20 for frame in sequence)
    assert sequence[-1] == 0
sandbox = scope["ShelterShootingSandbox"]()
sandbox.fire()
assert sandbox.ammo == 7 and sandbox.mode == "fire"
sandbox.fire()
assert sandbox.shots == 1
clock[0] = .5
sandbox.tick()
assert sandbox.mode == "idle"
sandbox.reload()
assert sandbox.mode == "reload"
sandbox.fire()
assert sandbox.shots == 1
clock[0] = 2.0
sandbox.tick()
assert sandbox.mode == "idle" and sandbox.ammo == 8
print("PASS: 20 RGBA frames, animation ranges, fire lockout, reload and idle return")