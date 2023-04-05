# -*- coding: utf-8 -*-
import pickle
from random import *
from utils import *
import numpy as np

class Gene:
    def __init__(self):
        self.direction = randint(0, 3)

    def getDirection(self):
        return self.direction
