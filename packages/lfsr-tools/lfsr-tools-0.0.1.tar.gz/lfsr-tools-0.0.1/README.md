# lfsr-tools
Tools for pseudo-random number sequence generation and LFSR recovery.

## Summary
This repository contains two basic classes: 
- LFSR
- BerlekampMassey

### LFSR
The LFSR class is a linear feedback shift register (LFSR) that creates a pseudo-random number (PN) sequence from a supplied generator polynomial. This generator polynomial specifies the LFSR architecture which determines what bit is fed back into the register. The LFSR-generated sequence should be obtained either by using an LFSR object as an iterator or using its `next_state` method.

#### Conventions
A polynomial is represented in _big endian_ format. For example, the primitive polynomial
$$x^4+x^3+1$$
is represented with its coefficients as
$$[1 0 0 1 1].$$
In other words, the coefficient $c_0$ that multiplies $x^0$ is in the zeroth place of the array that specifies the generator polynomial. Similarly, the coefficient $c_N$ that multiplies $x^N$ is in the $N$th place of the array that specifies the generator polynomial. 

The bit sequence that instantiates an LFSR object is specified in canonical order, so in the sequence 
$$[1 1 1 1 0 0 0 ... 0]$$
the bit that comes first in time at position zero is $1$ and the last bit of a sequence in position $M$ is, in this example, $0$. A seed is likewise explicitly specified on object instantiation or the implicit value of $[1 0 0 ...]$ is assumed.

### BerlekampMassey
This class implements the seminal algorithm developed in 1967 by Elwyn Berlekamp and later recognized for its application to LFSRs by James Massey. An object of this class is instantiated on a bit sequence $s$ and returns a shortest-length polynomial that can generate it.

#### Intuition
Many examples and explanations exist illuminating the Berlekamp-Massey Algorithm and so only an intuition for how the algorithm works is provided here. 

Suppose there is a black box that generates bits from a PN sequence which cannot be opened. Only the bits it generates can be observed. Assuming the black box generates its bits via a LFSR, the architecture of the lfsr can be recovered by designing a parallel LFSR which attempts to match the generated sequence $s$ which its own sequence $\hat{s}$. When the guess is wrong the LFSR architecture is updated so that the guess would have been correct and the process continues. The real magic of this algorithm is in putting forth an optimal architecture (specified by polynomial) update that keeps the LFSR length and computational burden to a minimum. An explanation of this magic is beyond the scope of this README.

## LFSR Example
Suppose an LFSR specified with the primitive polynomial $x^4+x^3+1$ is desired. Such an LFSR is illustrated below where the $+$ operator is addition in GF(2) (i.e., exclusive-or).

```
   ┌──┐   ┌──┐   ┌──┐   ┌──┐   ┌──┐
┌─►│0 ├──►│1 ├──►│1 ├──►│1 ├─┐►│1 ├─┐
│  └──┘   └──┘   └──┘   └──┘ │ └──┘ │
│                            │      │
│                          ┌─▼─┐    │
└──────────────────────────┤ + │◄───┘
                           └───┘```

Instantiation of the LFSR and polynomial recovery is accomplished via
```python
from lfsr_tools import LFSR, BerlekampMassey

polynomial = [1 1 0 0 1]
lfsr = LFSR(polynomial)
sequence = [bit for bit in lfsr] #Sequence generation via iterator

bkm = BerlekampMassey(sequence)
bkm.estimate_polynomial()
print(f"The generator polynomial is: {[1 1 0 0 1]}")
``` 