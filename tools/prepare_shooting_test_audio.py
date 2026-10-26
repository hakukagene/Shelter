"""Small original, procedural placeholder effects for the isolated gun demo."""
import math
from pathlib import Path
import random
import struct
import wave

DESTINATION = Path(__file__).resolve().parents[1] / 'game/audio/shooting_test'
RATE = 22050

def save(name, duration, signal):
    samples = []
    for i in range(int(duration * RATE)):
        t = i / RATE
        # Fade the final tail to avoid an end-of-file click.
        value = signal(t) * min(1.0, max(0.0, (duration - t) / .015))
        samples.append(struct.pack('<h', int(max(-.95, min(.95, value)) * 32767)))
    with wave.open(str(DESTINATION / name), 'wb') as output:
        output.setnchannels(1)
        output.setsampwidth(2)
        output.setframerate(RATE)
        output.writeframes(b''.join(samples))

def main():
    DESTINATION.mkdir(parents=True, exist_ok=True)
    randomizer = random.Random(751)
    def shot(t):
        noise = randomizer.uniform(-1, 1)
        attack = min(1, t / .0008)
        return attack * (.72 * noise * math.exp(-t * 31)
            + .28 * math.sin(2 * math.pi * (75 * t - 35 * t * t)) * math.exp(-t * 19))
    def clicks(t, moments):
        return sum((.32 * randomizer.uniform(-1, 1) + .13 * math.sin(2 * math.pi * 1700 * (t - at)))
            * math.exp(-(t - at) * 100) for at in moments if t >= at)
    save('shot.wav', .38, shot)
    save('reload.wav', 1.32, lambda t: clicks(t, (.08, .48, .91, 1.13)))
    save('empty.wav', .13, lambda t: clicks(t, (0,)))
    print('Prepared three procedural prototype sound effects.')

if __name__ == '__main__':
    main()
