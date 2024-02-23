from typing import Optional

import numpy as np
from numpy.typing import NDArray, ArrayLike

DEFAULT_CORRELATION_MAPPING = 'bpsk'

def circular_autocorrelation(bits: NDArray, 
                             mode: Optional[str]=DEFAULT_CORRELATION_MAPPING,
                             ) -> NDArray:
    '''Computes the circular autocorrelation of a sequence 'bits' using 
    the Fourier method.
    '''
    return circular_correlation(bits, bits, mode)

def circular_correlation(x: NDArray, 
                         y: NDArray, 
                         mode: str=DEFAULT_CORRELATION_MAPPING,
                         ) -> NDArray:
    '''Computes circular cross correlation for two equal length sequences
    using the Fourier method. The only currently supported mapping type is 
    'bpsk' which maps 1 -> 1 and 0 -> -1. This parameter is reserved for 
    future use.
    '''
    if isinstance(x, list):
        x = np.array(x)
    if isinstance(y, list):
        y = np.array(y)
    modbits_x = x.copy()
    modbits_y = y.copy()
    if mode == 'bpsk':
        modbits_x[modbits_x==0] = -1
        modbits_y[modbits_y==0] = -1
    
    return np.fft.ifft(np.fft.fft(modbits_x) * np.conj(np.fft.fft(modbits_y)))


def find_most_significant_bit(bits: ArrayLike) -> int:
    ''' Finds the index of the most significant bit in an array.
    '''
    if isinstance(bits, list):
        bits = np.array(bits)
    return np.max(np.where(bits==1))