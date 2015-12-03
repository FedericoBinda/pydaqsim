'''signal class'''

class signal:
    '''signal class'''
    def __init__(self,ID=None,Type=None,arrival_time=None):
        self._ID = ID
        self.amplitude = []
        self.timevector = []
        self._type = Type
        self._arrival_time = arrival_time
        self.ampunit = None
        self.timeunit = None

    def SetAmpUnit(self,unit):
        allowed = ['V','a.u.']
        if unit in allowed:
            self.ampunit = unit
        else:
            print 'ERROR! unit not allowed!'
        
