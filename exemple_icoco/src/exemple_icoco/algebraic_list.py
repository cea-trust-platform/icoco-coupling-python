# -*- coding: utf-8 -*-
"""
Two 1D Thermal-hydraulics channel with a "one cell" heated solid in between.
"""
import numpy as np

class Algebraic_list:
    def __init__(self, data):
        self._array = np.array(data)

    def get_data(self):
        return self._array

    def clone(self):
        return self._array.copy()

    def copy(self, data):
        np.copyto(dst=self._array, src=data)

    def normMax(self):
        return np.linalg.norm(self._array, ord=np.inf)

    def norm1(self):
        return np.linalg.norm(self._array, ord=1)

    def norm2(self):
        return np.linalg.norm(self._array, ord=2)

    def __add__(self, data):
        return self._array + data

    def __iadd__(self, data):
        self._array += data
        return self

    def __sub__(self, data):
        return self._array - data

    def __isub__(self, data):
        self._array -= data
        return self

    def __mul__(self, scalar):
        return self._array * scalar

    def __imul__(self, scalar):
        self._array *= scalar
        return self
