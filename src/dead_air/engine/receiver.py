from dead_air.engine.signal_catalogue import SignalCatalogue, Reception


class Receiver:

    def __init__(self, catalogue: SignalCatalogue):
        self.catalogue = catalogue
        self.freq = 91.400

        self.unlocked = {"weather_broadcast", "empty_channel"}

    def unlock_signal(self, signal_id: str):
        self.unlocked.add(signal_id)

    def tune(self, freq: float) -> Reception:
        self.freq = freq
        r = self.catalogue.detect(freq)
        if r.signal is not None and r.signal.id not in self.unlocked:
            return Reception(signal=None, strength=0.08, offset=r.offset)
        return r

    def get_curr_reception(self) -> Reception:
        return self.catalogue.detect(self.freq)
