import numpy as np
from hypothesis import strategies as st
from hypothesis import given

from lfsr_tools import LFSR, PolynomialError, SeedError
import lfsr_tools.utils as utils
from lfsr_tools.lfsr_config import *

@st.composite
def poly_seed_strategy(draw, 
                       poly_st=st.lists(st.sampled_from([0, 1]), min_size=2, max_size=32),
                       ):
    ''' This composite strategy first draws a polynomial then a seed that is of length 
    one less than the polynomial.
    '''
    poly = draw(poly_st)
    seed_st = st.lists(st.sampled_from([0, 1]), min_size=len(poly)-1, max_size=len(poly)-1)
    seed = draw(seed_st)

    return poly, seed

@given(poly_seed_strategy())
def test_lfsr_instantiation(poly_seed):
    ''' This test checks LSFR instantiation with various polynomial/seed combinations.
    Edge cases with reducible polynomials, polynomials with 0 coefficients in the MSB
    positions, and all zero seeds are also checked.
    '''
    poly, seed = poly_seed
    try:
        lfsr = LFSR(poly=poly,
                    seed=seed,
                    )
        for i, j in zip(lfsr.state, seed):
            assert i == j
        
        assert len(lfsr) == len(lfsr.state) # check __len__

    except PolynomialError:
        '''Degenerate polynomials are either all zero or only have a 1 in the LSBs place.'''
        assert (np.sum(poly) == 0) or ((poly[0]==1) and (np.sum(poly)==1))

    except SeedError:
        '''Bad seeds are all zero, everything else is fine.'''
        extended_seed = np.r_[0, seed] #Extend the seed to the same length as the polynomial
        poly_mask = np.zeros(len(poly)).astype(int)
        poly_mask_idx = utils.find_most_significant_bit(poly)
        poly_mask[:poly_mask_idx+1] = 1
        test_string = extended_seed & poly_mask #
        assert np.sum(test_string) == 0 #Check the remaining seed bits to make sure there is at least one remaining nonzero bit


def test_lfsr_iteration(poly_sets = [POLY1, POLY2, POLY3, POLY4, POLY5]):
    ''' Check that the correct m-sequence is output for each primitive 
    polynomial up to order five.
    '''
    def check_correlation_property(bits):
        corr = utils.circular_autocorrelation(bits, mode='bpsk')
        zerolag = (int(corr[0])==len(corr))
        nonzerolag = np.all(np.isclose(np.real(corr[1:]), -1))

        assert zerolag and nonzerolag

    for poly_set in poly_sets:
        for poly in poly_set:
            lfsr = LFSR(poly=poly)
            bits = []
            for bit in lfsr: #Test __iter__
                bits.append(bit)
            
            assert len(bits) == lfsr.max_seq_len #Check for correct number of states
            assert np.sum(bits) == 2**(len(lfsr)-1) #Check balance property
            check_correlation_property(bits) # Checks correlation property