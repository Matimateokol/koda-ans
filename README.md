# koda-ans
Asymmetric Numeral System codec implementation.


### algorithm explanation
N - interval size
R - renormalization size

uses the koding algorithm:

C(xi, s) = |_(xi / f(s) << n) + (xi % f(s)) + cdf(s)
D(xi+1, s) = f(s) * (xi+1 >> n) + (xi+1 & mask) - cdf(s) where mask = 2^n-1


### TESTS
Example:

``` python3 -m tests.entropy_tests ```