from pathlib import Path

import numpy as np
import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
AUDIO_DIR = ROOT / "assets" / "audio"

SOURCE = AUDIO_DIR / "empty_channel.wav"
OUTPUT = AUDIO_DIR / "empty_channel_clue.wav"

DIGITS = {
    "3": [
        "11110",
        "00001",
        "00001",
        "01110",
        "00001",
        "00001",
        "11110",
    ],
    "1": [
        "00100",
        "01100",
        "00100",
        "00100",
        "00100",
        "00100",
        "01110",
    ],
    "7": [
        "11111",
        "00001",
        "00010",
        "00100",
        "01000",
        "01000",
        "01000",
    ],
    "4": [
        "00010",
        "00110",
        "01010",
        "10010",
        "11111",
        "00010",
        "00010",
    ],
}


def main():
    audio, sample_rate = sf.read(SOURCE)

    if audio.ndim == 2:
        audio = audio.mean(axis=1)

    audio = audio.astype(np.float32)

    clue = np.zeros_like(audio)

    start_time = 5.0
    column_duration = 0.10
    tone_duration = 0.085

    # Seven frequency rows, separated clearly.
    frequencies = [
        3500,
        3050,
        2600,
        2150,
        1700,
        1250,
        800,
    ]

    columns = []

    for digit in "3174":
        for column in range(5):
            columns.append([DIGITS[digit][row][column] == "1" for row in range(7)])

        # Space between digits
        columns.append([False] * 7)

    fade_samples = int(sample_rate * 0.008)
    tone_samples = int(sample_rate * tone_duration)

    fade_in = np.linspace(0, 1, fade_samples, dtype=np.float32)

    fade_out = np.linspace(1, 0, fade_samples, dtype=np.float32)

    envelope = np.ones(tone_samples, dtype=np.float32)
    envelope[:fade_samples] = fade_in
    envelope[-fade_samples:] = fade_out

    for column_index, rows in enumerate(columns):
        column_start = start_time + column_index * column_duration

        sample_start = int(column_start * sample_rate)
        sample_end = sample_start + tone_samples

        if sample_end > len(clue):
            raise ValueError("Audio is too short for the clue.")

        time = np.arange(tone_samples) / sample_rate

        for row, active in enumerate(rows):
            if not active:
                continue

            tone = 0.045 * np.sin(2 * np.pi * frequencies[row] * time) * envelope

            clue[sample_start:sample_end] += tone

    mixed = audio + clue

    peak = np.max(np.abs(mixed))

    if peak > 0.98:
        mixed *= 0.98 / peak

    sf.write(OUTPUT, mixed, sample_rate, subtype="PCM_16")

    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
