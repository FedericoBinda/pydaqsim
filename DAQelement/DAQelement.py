from .. import signal

class DAQelement:
    def __init__(self,name):
        self.name = None

    def process(self,s):
        if not isinstance(s,signal.signal):
            raise TypeError('Wrong object type parsed to function. Function expected a "signal" object.')
        s.amplitude = 2*s.amplitude
