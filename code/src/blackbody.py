import numpy as np
from utils.utils import set_root_dir
set_root_dir()

class BlackBody(object):
    def __init__(self,
                 **kwargs):
        super(BlackBody, self).__init__()
        self.temperature = np.nan
        self.flux = np.nan
