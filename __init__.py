'''
pyDAQsim
========

Simulation of the data acquisition chain of a detector
'''

# enable tab completion
# ---------------------

import rlcompleter, readline
readline.parse_and_bind('tab: complete')
del rlcompleter, readline

from DAQelement import *
from signal import *
