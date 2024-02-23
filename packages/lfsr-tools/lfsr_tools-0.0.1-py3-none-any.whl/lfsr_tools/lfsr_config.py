import numpy as np

# Known primitive polynomials listed by polynomial order up to order 5
# Source: https://mathworld.wolfram.com/PrimitivePolynomial.html
# Format is [LSB, ..., MSB]
# Example: x^4+x^3+1 -> [1, 0, 0, 1, 1]
POLY1 = np.array([[1, 1]])
POLY2 = np.array([[1, 1, 1]])
POLY3 = np.array([[1, 0, 1, 1],
                  [1, 1, 0, 1],
                  ])
POLY4 = np.array([[1, 1, 0, 0, 1],
                  [1, 0, 0, 1, 1],
                  ])
POLY5 = np.array([[1, 0, 1, 0, 0, 1],
                  [1, 1, 1, 1, 0, 1],
                  [1, 0, 0, 1, 0, 1],
                  [1, 1, 0, 1, 1, 1],
                  [1, 0, 1, 1, 1, 1],
                  [1, 1, 1, 0, 1, 1],
                  ])