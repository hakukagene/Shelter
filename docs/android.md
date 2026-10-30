# Android APK

Android uses the author's supplied bunker-door `icon.ico` artwork through the
root `android-icon_foreground.png` (transparent 432×432) and
`android-icon_background.png` (opaque 432×432). The foreground is inset so
launcher masks can crop the surrounding background without cutting off the door.
Ren'Py generates the launcher icon sizes, including older non-adaptive icons.

The root `android-presplash.jpg` is the 1920×1080 **АЧААЛЖ БАЙНА...** startup
screen. RAPT displays it while the native app starts, before the main menu; it
does not add an artificial delay or replace the story intro. Its black border
fills extra space on wider/taller phones without stretching the artwork.
`android.json` already enables `update_icons` and `update_always`, so both icon
and startup art are picked up by the next build. Rebuild and install the updated
APK to see them; existing installed APKs do not update their bundled images.

The assets are ready to package without Python/Pillow on the build machine.
To regenerate them after editing the source art, use
`python tools/prepare_android_branding.py --presplash path/to/loading-art.png`.
Omit `--presplash` to regenerate just the icon layers. See
`tools/art/android-branding.md` for the image-generation prompt and provenance.

The Android build uses Ren'Py **8.5.3** and produces a signed universal APK in
`dist/android/`. Copy the APK to an Android phone and open it to install.
If Android asks, allow installation from the app used to open that file.

The app is named **Хорогдох байр**, with package ID `mn.shelter.game`, version
`1.0`, and landscape orientation. It supports Android 5.0+ with OpenGL ES 3.0;
ARM64, ARMv7, and x86_64 libraries are included. Videos, fonts, and subtitles
are included in the APK; no separate media download is needed.

Rebuild from the project directory in PowerShell:

```powershell
.\tools\build_android.ps1
```

For a fresh toolchain, install the matching Android support in the Ren'Py
Launcher, then run `.\tools\build_android.ps1 -Setup`. This downloads a portable
JDK 21, installs Android SDK dependencies, and accepts their licenses.
Use `-RenpySdk 'C:\path\to\renpy-8.5.3-sdk'` for a different SDK location.
The local JDK and Gradle cache live under `.android-build/`.

Keep a backup of the root `android.keystore` and `bundle.keystore` files.
Future updates must use the same signing key and package ID. RAPT assigns
the build timestamp as the Android version code (or `numeric_version` from
`android.json`, if greater); update `version` for the displayed release number.
Keys, tool caches, tests, and previous packages are excluded from distributions
and Git.

The initial APK passed signature, ZIP integrity, and 16 KB alignment checks.
Start → intro → subtitles → skip → first visitor also passed in Ren'Py's
phone/touch emulation. Installation and playback on physical Android hardware
have not been tested.
