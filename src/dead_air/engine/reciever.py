from dead_air.engine.signal_catalogue import SignalCatalogue, Reception


class Reciver:

    def __init__(self, catalogue: SignalCatalogue):
        self.catalogue = catalogue
        self.freq = 91.400

    def tune(self, freq: float) -> Reception:
        self.freq = freq
        return self.catalogue.detect(freq)

    def get_curr_reception(self) -> Reception:
        return self.catalogue.detect(self.freq)
