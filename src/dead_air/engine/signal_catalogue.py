import json

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Signal:
    id: str
    name: str
    freq: float
    tolerance: float
    peak_strength: float
    audio_file: str
    desc: str


@dataclass(frozen=True)
class Reception:
    signal: Signal | None
    strength: float
    offset: float | None


class SignalCatalogue:
    def __init__(self, singals: list[Signal]):
        self.signals = sorted(singals, key=lambda singal: singal.freq)

        ids = [signal.id for signal in self.signals]

        if len(ids) != len(set(ids)):
            raise ValueError("Duplicate")

        freqs = [signal.freq for signal in self.signals]

        if len(freqs) != len(set(freqs)):
            raise ValueError("Duplicate")

    @classmethod
    def load(cls, path: Path):
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        signals = [Signal(**entry) for entry in data["signals"]]

        return cls(signals)  # why is spelling signal harddd

    def detect(self, freq: float) -> Reception:
        cand = []

        for sig in self.signals:

            off = abs(freq - sig.freq)

            if off <= sig.tolerance:
                cand.append((off, sig))

        if not cand:
            return Reception(signal=None, strength=0.02, offset=None)

        off, sig = min(cand, key=lambda c: c[0])

        deviation = off / sig.tolerance

        strength = sig.peak_strength * (1.0 - 0.75 * deviation)

        return Reception(signal=sig, strength=strength, offset=off)
