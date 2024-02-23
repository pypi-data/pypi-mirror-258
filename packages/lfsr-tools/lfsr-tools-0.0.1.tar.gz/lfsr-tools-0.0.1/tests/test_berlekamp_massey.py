import numpy as np
from hypothesis import strategies as st
from hypothesis import given
import pytest

from lfsr_tools import BerlekampMassey, BerlekampMasseyError, LFSR
from lfsr_tools.lfsr_config import *


@given(st.lists(st.sampled_from([0,1]), min_size=0, max_size=64))
def test_bm_instantiation(sequence):
    try:
        bkm = BerlekampMassey(sequence=sequence)
    except BerlekampMasseyError:
        assert len(sequence)==0


def test_bm_primitive_impl(poly_sets = [POLY1, POLY2, POLY3, POLY4, POLY5]):
    ''' Generate a sequence with a LFSR and then verify that the polynomial 
    can be recovered with Berlekamp Massey. Tests all primitive polynomials
    of order 5 or less.
    '''
    for poly_set in poly_sets:
        for polynomial in poly_set:
            lfsr = LFSR(poly=polynomial)
            sequence = [bit for bit in lfsr]
            bkm = BerlekampMassey(sequence=sequence)
            bkm.estimate_polynomial()
            assert np.all(bkm.est_poly == polynomial)


@given(st.lists(st.sampled_from([0,1]), min_size=2, max_size=6).filter(lambda x: x[0] + x[-1] == 2))
def test_bm_nonprimitive_impl(poly):
    ''' Tests selected (primitive or nonprimitive) polynomials up to and including degree 5.
    Only polynomials of the form 1 + ... + x^(max_size-1) are allowed. The Berlekamp-Massey
    implementation fails otherwise.
    '''
    lfsr = LFSR(poly=poly)
    sequence = [bit for bit in lfsr]
    bkm = BerlekampMassey(sequence=sequence)
    bkm.estimate_polynomial()
    assert np.all(bkm.est_poly == poly)


@pytest.mark.xfail(reason='The Berlekamp-Massey implementation fails for polynomials where the order 0 coefficient is 0.')
@given(st.lists(st.sampled_from([0,1]), min_size=2, max_size=6).filter(lambda x: x[-1]==1))
def test_bm_nonprimitive_degenerate_impl(poly):
    ''' Tests all (primitive or nonprimitive) polynomials up to and including degree 5.
    '''
    lfsr = LFSR(poly=poly)
    sequence = [bit for bit in lfsr]
    bkm = BerlekampMassey(sequence=sequence)
    bkm.estimate_polynomial()
    assert np.all(bkm.est_poly == poly)