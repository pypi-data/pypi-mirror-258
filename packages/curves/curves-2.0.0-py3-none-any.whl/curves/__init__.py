# Copyright(c) 2019 Jake Fowler
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import platform

os = platform.system()
# On non-Windows platform try to load Core CLR, rather than the default behaviour which is to load Mono.
if os != 'Windows':
    from pythonnet import load

    try:
        load('coreclr')
    except:
        print('Could not load Core CLR runtime, on non-Windows OS, so falling back to Mono.')

from curves.bootstrap import bootstrap_contracts
from curves.max_smoothness_spline import max_smooth_interp
from curves.hyperbolic_tension_spline import hyperbolic_tension_spline, KnotPositions
from curves._common import FREQ_TO_PERIOD_TYPE
from curves.__version__ import __version__