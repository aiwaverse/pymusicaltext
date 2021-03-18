from pymusicaltext.core.constants import (
    BPM_MAX,
    BPM_MIN,
    INSTRUMENT_MAX,
    INSTRUMENT_MIN,
    OCTAVE_MAX,
    OCTAVE_MIN,
    VOLUME_MAX,
    VOLUME_MIN,
)


class BasicMidiInfo:
    def __init__(self, octave: int = 0, volume: int = 0) -> None:
        self._octave: int = octave
        self._volume: int = volume

    @property
    def octave(self) -> int:
        return self._octave

    @octave.setter
    def octave(self, o: int) -> None:
        """
        Checks if o is in correct range for octave
        sets if it is, otherwise uses the limits
        """
        if o > OCTAVE_MAX:
            self._octave = OCTAVE_MAX
        elif o < OCTAVE_MIN:
            self._octave = OCTAVE_MIN
        else:
            self._octave = o

    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, v: int) -> None:
        """
        Checks if v is in correct range for volume
        sets if it is, otherwise uses the limits
        """
        if v > VOLUME_MAX:
            self._volume = VOLUME_MAX
        elif v < VOLUME_MIN:
            self._volume = VOLUME_MIN
        else:
            self._volume = v

    def __str__(self) -> str:
        return f"Octave: {self.octave}\nVolume: {self.volume}\n"


class AdvancedMidiInfo(BasicMidiInfo):
    def __init__(
        self,
        octave: int = 0,
        volume: int = 0,
        instrument: int = 0,
        bpm: int = 0,
    ) -> None:
        super().__init__(octave=octave, volume=volume)
        self._instrument: int = instrument
        self._bpm: int = bpm

    @property
    def instrument(self) -> int:
        return self._instrument

    @instrument.setter
    def instrument(self, i: int) -> None:
        """
        Checks if i is in correct range for instrument
        sets if it is, otherwise uses the limits
        """
        if i > INSTRUMENT_MAX:
            self._instrument = INSTRUMENT_MAX
        if i < INSTRUMENT_MIN:
            self._instrument = INSTRUMENT_MIN
        else:
            self._instrument = i

    @property
    def bpm(self) -> int:
        return self._bpm

    @bpm.setter
    def bpm(self, bp: int) -> None:
        """
        Checks if bp is in correct range for instrument
        sets if it is, otherwise uses the limits
        """
        if bp > BPM_MAX:
            self._bpm = BPM_MAX
        elif bp < BPM_MIN:
            self._bpm = BPM_MIN
        else:
            self._bpm = bp

    def __str__(self) -> str:
        return (
            super().__str__()
            + f"Instrument: {self.instrument}\nBPM: {self.bpm}"
        )
