# -*- coding: utf-8 -*-
from papers.configs import configs
from papers.models import Source

def build(url, **args):
    configurations = {
        **args,
        **configs
    }
    
    return Source(url, args=configurations)

