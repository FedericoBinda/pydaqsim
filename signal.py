'''signal class'''

class signal:
    '''signal class'''
    def __init__(self,ID=None,Type=None,arrival_time=None):
        self._ID = ID
        self._type = Type
        self._arrival_time = arrival_time
        self.amplitude = []
