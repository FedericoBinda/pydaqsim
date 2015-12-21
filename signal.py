'''signal module'''

import numpy as np

class signal:
    '''signal class'''
    def __init__(self,ID=None,Type=None,arrival_time=None,amplitude=[]):
        self._ID = ID
        self._type = Type
        self._arrival_time = arrival_time
        self.amplitude = amplitude

class generator:
    '''signal generator'''
    def __init__(self,name = '', types=['gamma','neutron']):
        self._name = name
        self._types = types
        self._timedist = {}
        self._energydist = {}
        for t in types:
            self._timedist[t] = {'time' : [] , 'prob': []}
            self._energydist[t] = {'energy' : [] , 'prob' : []}

    def __repr__(self):
        return self._name

    def __str__(self):
        att = [(a,str(getattr(self,a))) for a in dir(self) if not callable(getattr(self,a)) and not a.startswith('__')]
        s = ''
        for a in att:
            s += '\n'
            if a[0][0] == '_':
                s += a[0][1:] 
            else:
                s += a[0]
            s += ' = ' + str(a[1])
        s += '\n'
        return s

class scintillator(generator):
    '''scintillator class'''
    def __init__(self, name = '', types=['gamma','neutron'], k=None, lc=None, qeff=None):
        generator.__init__(self,name=name,types=types)
        self._k = k
        self._lc = lc
        self._qeff = qeff

    def generate(self, Type, n):
        k = self._k
        lc = self._lc
        qeff = self._qeff
        if Type not in self._types:
            raise TypeError('Pulse type not present in scintillator''s type list')
        energy = self._energydist[Type]['energy']
        spectrum = self._energydist[Type]['prob']
        t = self._timedist[Type]['time']
        amp = self._timedist[Type]['prob']

        # Convert energy axis to nphots axis
        # ------

        nphots_axis = energy * k

        # Generate nphots spectrum
        # ------

        nphots = np.random.choice(nphots_axis, n, p = spectrum)

        # Randomize nphots according to poisson distribution and
        # including the quantum efficiency qeff and 
        # the light collection efficiency lc
        # ------

        mynphots = np.random.poisson(nphots*qeff*lc, n)

        # Generate the signals list
        # ------

        mysignals = [signal(Type=Type,amplitude=np.random.choice(t, numphots, p = amp)) for numphots in mynphots]
    
        return mysignals
