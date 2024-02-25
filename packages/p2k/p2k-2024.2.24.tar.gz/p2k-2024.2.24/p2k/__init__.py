from .proxy import ProxyRecord, ProxyDatabase
from . import utils

from .visual import (
    set_style,
    showfig,
    closefig,
    savefig,
)
set_style(style='journal', font_scale=1.2)

# get the version
from importlib.metadata import version
__version__ = version('p2k')


# mute future warnings from pkgs like pandas
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
        
# mute the numpy warnings
warnings.simplefilter('ignore', category=RuntimeWarning)