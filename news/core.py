# -*- coding: utf-8 -*-
from .configs import configs
from .models import Source

def build(url, **args):
    configurations = {
        **args,
        **configs
    }
    
    return Source(url, args=configurations)

