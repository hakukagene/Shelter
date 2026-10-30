# Standalone handgun prototype

Development sandbox only: the main-menu entry appears when `config.developer`
is true (running from the Ren'Py SDK) and is hidden in release builds.

Choose **Буудлагын туршилт** from the main menu to start the separate
`shelter_shooting_test` label in `game/shooting_test.rpy`. Click/tap a paper
target or use the **Буудах** button / Space. R or **Цэнэглэх** reloads the
magazine (currently seven rounds). Esc or **Буцах** returns to the menu.

Runtime sprites are in `game/images/shooting_test/sequence/`: one idle PNG,
ten firing PNGs, and **45 reload PNGs at 25 FPS** (1.8 seconds, 40ms per frame).
They have a shared transparent 600×500 canvas and a fixed pivot; the first and
last reload files match idle exactly to avoid an endpoint jump. The 43 interior
reload images are distinct. Handling, recoil, short pose dissolves and a new
sleeve extension are baked into the files, rather than recomposed during play.
These are offline animation frames built from the archived photographic poses,
not 45 separately painted anatomical poses. The old runtime sprites are removed.

Source poses remain under `tools/art/shooting-test/source-poses/`. The sleeve
extension was generated as a standalone transparent clothing asset with built-in
imagegen; its prompt is `tools/art/shooting-test/sleeve-extension.md`. Rebuild the
PNG sequence using the Ren'Py test command `test shelter_sprite_export`, then
restart the game so it discovers the new files. The development exporter is
`game/shooting_sprite_export.rpy`, excluded from release builds. Validate the
files with `python tools/check_shooting_sequence.py`.

The native playback suite is `shelter_shooting_checks`; screenshots, including
the repaired rack sleeve, are under `tmp/shooting-tests/`. Sprites are preloaded,
GPU transforms and small target/reticle textures are reused, and state completion
uses event deadlines instead of a repeating screen timer. Gameplay can redraw at
60 Hz while weapon animation holds each PNG for 40ms. The cadence test reports
render timing rather than a guarantee of GPU FPS on every device. The shared
gun pivot stays at (960,1080); aim tilts the barrel up to 12 degrees left/right.
The supplied door background remains under `game/images/shooting_test/`.
Procedural sound effects can be rebuilt with `tools/prepare_shooting_test_audio.py`.

The sandbox also spawns a frontal creature: it runs from the street to the
window, then repeatedly bangs on the steel door. Eight run sprites and eight
replacement alternating-fist sprites are under `game/images/shooting_test/monster/`.
The source/prompt pairs are `tools/art/shooting-test/monster-sheet.png` / `monster.md`
and `monster-alternating-sheet.png` / `monster-alternating.md`. Rebuild these with
`python tools/prepare_shooting_monster.py`. Pane clipping keeps the steel frame
in front of the creature. Each impact triggers the existing metal-door knock
and a short door shake on a separate sound channel. Three aimed hits make it
fade away; another approaches shortly afterward. **Дахин дайруулах** / T
restarts the approach. This feature remains inside the standalone test label.
The old four simultaneous-fist runtime images have been deleted. The new cycle
uses 24 timeline ticks at 25 FPS, with screen-left and screen-right contacts at
ticks 6 and 18. Each contact triggers its own knock and shake, 480ms apart.
Nonfatal hits do not rewind the approach clock, shrink the monster or interrupt
its stride/windup/strike timing. Successful hits trigger a restrained eight-frame
crimson particle burst at the aiming position, doubled in diameter (60–264 logical
pixels according to distance), clipped behind the steel door
with the creature. Sprites are under `game/images/shooting_test/blood/`; source
and imagegen prompt are `tools/art/shooting-test/blood-hit-sheet.png` and
`blood-hit.md`. Rebuild with `python tools/prepare_blood_hit.py`. Effects play at
25 FPS for 0.32 seconds, expire automatically and also appear on the fatal hit.
The creature smoothly emerges from shadow: RGB brightness increases from 10%
at the far end to 100% at the door, using the same smooth depth curve as movement.
Reusable GPU color transforms preserve sprite transparency and leave blood/HUD
brightness unchanged.
The creature follows three perspective lanes inside `SHOOTING_MONSTER_ROAD`.
Aiming now selects 35 authored perspective poses (7 yaw × 5 pitch) from
`images/shooting_test/aim35/`, each with idle and firing versions: 70 PNGs total.
Both crosshair axes ease toward their targets; frame selection updates at 25 FPS.
One opaque sprite is drawn at a time, with no gun rotation or silhouette dissolve.
The wrist base remains fixed. The existing 45-frame reload is retained.
Sources and built-in imagegen prompts are in `tools/art/shooting-test/aim35/`.
Export with `python tools/prepare_aim35.py`; it splits and resizes the atlas cells,
detects row gutters, preserves alpha, and verifies 70 distinct exported PNGs.
The door starts with 100 HP. Each alternating claw swipe deals 10 damage at its
contact tick, including elapsed contacts if an update is delayed. At zero HP,
attacks and firing stop. T / restart restores the door; automatic monster respawn
preserves accumulated damage. The HUD shows door HP and a health bar.
Waves repeat 1, 2, 1, 3 creatures. Each creature has its own route, stride, hitbox,
three-hit health and blood effect; the whole crowd shares door HP and totals.
Head hits deal 1.5 health and body hits deal 1 health against 3 total health:
two headshots or three body shots kill a creature. Mixed hits accumulate on the
same health pool. The smaller pink head region scales with the creature and is
clipped by the same glass panes as body hits; steel bars never count as hits.
Only the nearest overlapping creature takes a bullet. A cleared wave advances
after the final death delay; HP remains depleted between waves. T resets to the
first solo wave and restores door HP. N / the next-wave button previews the next
formation. Creatures are depth sorted and clipped behind the door together.
The replacement open-claw poses are `images/shooting_test/monster/claw-*.png`.
Source atlases and built-in imagegen prompts are `tools/art/shooting-test/aim-directions*`
and `monster-claw*`; export with `python tools/prepare_directional_claw_sprites.py`.
Every approach alternates between two and three smooth adjacent-lane changes;
successive attacks end left/center/right. Feet reach the actual polygon's near
edge (currently y=900), rather than a separate hardcoded y=604. Sprite size grows
with the new depth while the near head stays at y=316. Forward motion slows at
the edge, followed by a 200ms raised-fist windup and then door strikes. The HUD
shows completed/total lane changes. Debug routes rebuild for the current plan,
highlight its selected route, and finish at the same green edge as the creature.
Hit detection uses the same moving position and scale.
Debug overlays start enabled in the sandbox. **D** / **Debug** toggles them:
green is the street boundary, blue traces the three actual curved routes,
red outlines the full monster hitbox, and yellow shows the hittable parts after
clipping against the glass panes. The overlay and shooting share the same
`hit_bounds` / `hit_rectangles` geometry; steel mullions remain non-hittable.
