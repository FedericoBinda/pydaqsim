from .. import signal
import numpy as np
from scipy import stats, constants
from scipy import signal as spsig

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

class pmt(DAQelement):

    def __init__(self,name='',ndynodes=None,delta=None,sigma=None,transittime=None):
        DAQelement.__init__(self,name=name)
        self._ndynodes = ndynodes
        self._delta = delta
        self._sigma = sigma
        self._transittime = transittime

    def process(self,s,t):
        '''s.amplitude should be time arrival at the pmt'''

        DAQelement.process(self,s)
        
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

class cable(DAQelement):
    '''cable class'''
    def __init__(self,name='',cutoff=None,impedance=None,noise_lvl=None):
        DAQelement.__init__(self,name=name)
        self._cutoff = cutoff
        self._impedance = impedance
        self._noise_lvl = noise_lvl

    def process(self,s,t):

        DAQelement.process(self,s)

        sampling_freq = 1./(t[1]-t[0]) # GHz
        Wn = (1./(2*np.pi))*(self._cutoff/sampling_freq)
        b, a = spsig.butter(1, Wn, 'low')

        noise = np.random.normal(0,self._noise_lvl,len(s.amplitude))
        s.amplitude = spsig.lfilter(b,a,s.amplitude) * self._impedance + noise
        
class digitizer(DAQelement):
    '''digitizer class'''
    def __init__(self,name='',sampfreq=None,nbits=None,minV=None,maxV=None,
                 th_lvl=None,th_on=False):
        DAQelement.__init__(self,name=name)
        self._sampfreq = sampfreq
        self._nbits = nbits
        self._minV = minV
        self._maxV = maxV
        self._th_lvl = th_lvl
        self._th_on = th_on
        self.update_values()

    def update_values(self):
        try:
            self._codes = np.linspace(self._minV,self._maxV,2**self._nbits)
            self._dV = (self._maxV- self._minV) / 2**self._nbits
            self._th_V = self._th_lvl * self._dV
        except:
            self._codes = None
            self._dV = None
            self._th_V = None
            

    def process(self,s,t):

        DAQelement.process(self,s)

        dt = t[1] - t[0]
        freq = 1. / dt
        ratio = int(freq / self._sampfreq)

        if self._th_on:
            try:
                trigger = np.where(s.amplitude >= self._th_V)[0][0]
            except IndexError:
                s.amplitude = np.array([])
                return
            pretrig = s.amplitude[trigger::-ratio][::-1]
            posttrig = s.amplitude[trigger+ratio::ratio]
            newpulse = np.append(pretrig,posttrig)
        else:
            newpulse = s.amplitude[::ratio]
            
        s.amplitude = np.digitize(newpulse, self._codes)

class chain:
    'chain class'
    def __init__(self,name='',elements=[]):
        self._name = name
        self._elements = elements

    def add_element(self,e):
        if not isinstance(e,DAQelement):
            raise TypeError('Wrong object type parsed to function. Function expected a "DAQelement" object.')
        self._elements.append(e)

    def pop_element(self,index):
        self._elemenents.pop(index)

    def process(self,s,t):
        if type(s) is list:
            for si in s:
                for e in self._elements:
                    e.process(si,t)
        else:
            for e in self._elements:
                e.process(s,t)
