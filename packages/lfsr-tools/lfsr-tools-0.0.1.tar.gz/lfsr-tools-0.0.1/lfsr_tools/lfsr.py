from collections import deque
from warnings import warn
from functools import reduce
from operator import xor
from typing import Optional

import numpy as np
from numpy.typing import ArrayLike


class PolynomialError(ValueError):
    pass

class SeedError(ValueError):
    pass


class LFSR():
    def __init__(self, 
                 poly: ArrayLike,
                 seed: Optional[ArrayLike] = None,
                 ):
        ''' Linear feedback shift register implementation. The shift register can be any length and the 
        notation is in little endian format. For instance, to specify the primitive polynomial:
            x^4+x^3+1
        you would indicate poly=[1 0 0 1 1]. The same notation is required for seed. Seed must
        have at least one non-zero value otherwise the register will continually maintain the all 
        zeros state.
        '''
        poly, seed = self._parameter_checker(poly, seed)
        self.state = seed #State of the shift register
        self.poly = poly #Polynomial generator
        self.seed = seed #The initial seed
        self.iterations = 0 #Number of bits shifted through the register
        self.max_seq_len = 2**len(self.state) - 1 #The maximum possible sequence length given the shift register size. The sequence will only reach this length if the provided polynomial is primitive.
    
    def __len__(self):
        return len(self.state)
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.iterations <= self.max_seq_len - 1:
            self.iterations += 1
            return self.next_state()
        else:
            raise StopIteration
        
    def _parameter_checker(self, poly, seed):
        '''Called by __init__, this method performs various checks and operations 
        to ensure the LFSR register size is the smallest realiziable by the 
        generator polynomial and that the provided seed is compatible with the 
        polynomial. PolynomialErrors or SeedErrors are raised when appropriate.
        '''
        if isinstance(poly, list):
            poly = np.array(poly)
        assert np.all((poly==1) ^ (poly==0)), 'The provided sequence must be include only valid numerical bits.'

        if (poly[0] != 1) or (poly[-1] != 1):
            warn('LFSR polynomial is reducible. Ensure you have provided the correct coefficients.')
            while poly[-1] == 0:
                poly = poly[:-1]
                if len(poly) <= 1:
                    raise PolynomialError('LFSR polynomial must be non-degenerate.')
                
        if seed is None:
            seed = np.zeros(len(poly)-1).astype(int)
            seed[0] = 1
        elif isinstance(seed, list):
            seed = np.array(seed)
            seed = seed[:len(poly)-1] # If the polynomial length was reduced due to the MSB not 1 then reduce also the seed by the same amount
        if not (np.all((seed==1) ^ (seed==0))): 
            raise SeedError('The provided seed must include only numerical bits.')
        if np.sum(seed) == 0:
            raise SeedError('The seed must have at least one bit as a 1.')

        return poly, seed
    
    def next_state(self):
        '''Essential method for rotating bits through the LFSR. This method also implements the
        LFSR internals specified by the generator polynomial.
        '''
        mask = self.poly[1:]
        in_bit = reduce(xor, mask & self.state)
        out_bit = self.state.pop()
        self.state.appendleft(in_bit)
        return out_bit

    #Class property list
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = deque(value)

    @property
    def poly(self):
        return self._poly
    
    @poly.setter
    def poly(self, value):
        self._poly = value

    @property
    def seed(self):
        return self._seed
    
    @seed.setter
    def seed(self, value):
        assert len(value) == len(self._state)
        self._seed = value

    @property
    def max_seq_len(self):
        return self._max_seq_len
    
    @max_seq_len.setter
    def max_seq_len(self, value):
        self._max_seq_len = value
