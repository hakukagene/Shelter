# Android icon and launch art

The author supplied `icon.ico` on 2026-10-22. It is byte-identical to the existing
root `icon.ico`. The Android foreground is a format/size conversion of its largest
256px frame, not regenerated artwork. The 240px source is centered on a transparent
432px canvas; an opaque charcoal 432px background completes the adaptive icon.
RAPT builds the per-density adaptive and legacy launcher icons from these layers.

Files consumed directly from the project root by Ren'Py Android packaging:

- `android-icon_foreground.png`
- `android-icon_background.png`
- `android-presplash.jpg` (1920×1080 RGB JPEG)

`android.json` already has `update_icons` and `update_always` enabled. No package
ID or signing keys change. Build again and install the APK to update its assets.
This is the native presplash while the app initializes, not a timed Ren'Py
splashscreen after startup. It has no fake percentage or added delay. The game
still opens its normal main menu and plays the story intro when Start is selected.

## Loading screen generation

Built-in ImageGen, compositing. References: the supplied ICO decoded to PNG and
`game/gui/shelter/main_menu/bunker.png`. The generated artwork was converted to
JPEG and fitted with black padding without distortion by
`tools/prepare_android_branding.py`. Pure black edges let RAPT fill extra screen
space consistently. The source ICO and desktop icon are unchanged.

Prompt:

> Create final Android loading screen for Mongolian horror game Shelter, 1920x1080 landscape. Reference 1 is exact icon identity: scratched steel bunker door, three-spoke circular locking wheel, red barred warning lamp and viewing hatch. Reference 2 is game menu style. Cinematic door embedded in dark concrete wall on left, red light, subtle mist, restrained amber highlights. Right: large distressed off-white title 'ХОРОГДОХ', below red 'БАЙР', matching menu lettering. Under title a thin red line then clean readable light-gray text exactly 'АЧААЛЖ БАЙНА...'. Keep all text within central 80% safe area. All perimeter fades fully to pure black with 24px solid black border for phone aspect ratios. Preserve door identity. No people, hands, weapons, percentage, progress bar, buttons, device frame, or extra text. Premium atmospheric photorealistic full-screen game loading art.

## Checks and scope

Checked the ICO identity, 432px foreground alpha and opaque background, 1920×1080
JPEG decoding, black perimeter pixels, enabled RAPT asset updates, and the final
artwork visually. The native Android toolchain and a physical phone are not
available in this workspace, so a new APK or on-device startup was not tested.

Reference: https://www.renpy.org/doc/html/android.html#icon-and-presplash-images
