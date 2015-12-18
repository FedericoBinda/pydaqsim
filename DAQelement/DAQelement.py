from .. import signal

class DAQelement:

    def __init__(self,name=''):
        self._name = name

    def __repr__(self):
        return self._name

    def test(self):
        att = [(a,str(getattr(self,a))) for a in dir(self) if not callable(getattr(self,a)) and not a.startswith('__')]
        return att
    def __str__(self):
        att = [(a,str(getattr(self,a))) for a in dir(self) if not callable(getattr(self,a)) and not a.startswith('__')]
        s = ''
        for a in att:
            if a[0][0] == '_':
                s += a[0][1:] 
            else:
                s += a[0]
            s+= ' = ' + str(a[1]) + '\n' 
        return s

    def process(self,s):
        if not isinstance(s,signal.signal):
            raise TypeError('Wrong object type parsed to function. Function expected a "signal" object.')
        s.amplitude = 2*s.amplitude

class PMT(DAQelement):
    def __init__(self,name='',ndynodes=None,delta=None,sigma=None,transittime=None):
        self._name = name
        self._ndynodes = ndynodes
        self._delta = delta
        self._sigma = sigma
        self._transittime = transittime

