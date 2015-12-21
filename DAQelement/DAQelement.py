from .. import signal
import numpy as np
from scipy import stats, constants

class DAQelement:

    def __init__(self,name=''):
        self._name = name

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

    def process(self,s):
        if not isinstance(s,signal.signal):
            raise TypeError('Wrong object type parsed to function. Function expected a "signal" object.')
        s.amplitude = 2*s.amplitude

class PMT(DAQelement):

    def __init__(self,name='',ndynodes=None,delta=None,sigma=None,transittime=None):
        DAQelement.__init__(self,name=name)
        self._ndynodes = ndynodes
        self._delta = delta
        self._sigma = sigma
        self._transittime = transittime

    def process(self,s,t):
        '''s.amplitude should be time arrival at the PMT'''

        if not isinstance(s,signal.signal):
            raise TypeError('Wrong object type parsed to function. Function expected a "signal" object.')
        
        ndynodes = self._ndynodes
        delta = self._delta
        sigma = self._sigma
        transittime = self._transittime
        pulse = s.amplitude

        # add poisson noise due to electron multiplication statistics
        # -------

        ww = (np.random.poisson(delta-1,len(pulse))+1) * delta**(ndynodes-1)

        # histogram the data
        # -------

        hist,bin_edges = np.histogram(pulse,bins=t,range=(t.min(),t.max()),weights=ww)

        # Prepare gaussian response for convolution
        # -------

        dt = t[1]-t[0]
        t2 = np.arange(-5*sigma,5*sigma,dt)
        y = stats.norm.pdf(t2, loc=0, scale=sigma)
        y /= sum(y)

        # Convolve pulse with gaussian response
        # -------

        newpulse = np.convolve(hist,y)#[:len(t)]

        # Include transit time
        # ------

        newpulse = np.append(np.zeros(int(transittime/dt)),newpulse)[:len(t)]

        # Convert the pulse from n_electrons to current
        # -----
    
        newpulse *= constants.e / (dt*1.e-9)
        s.amplitude = newpulse
