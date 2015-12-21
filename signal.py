'''signal class'''

class signal:
    '''signal class'''
    def __init__(self,ID=None,Type=None,arrival_time=None):
        self._ID = ID
        self._type = Type
        self._arrival_time = arrival_time
        self.amplitude = []

class generator:
    '''signal generator'''
    def __init__(self,name = '', types=['gamma','neutron']):
        self._name = name
        self._types = types
        self._pdfs = None

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

    
