ITERATIONS = 100
EXPECTED = 8939

from ppci.lang.python import jit



@jit
def mandelbrot() -> int:
    count = 0

    h = 150.
    Z = 0.0  ## Zr
    z = 0.0  ## Zi
    T = 0.0  ## Tr
    t = 0.0  ## Ti
    C = 0.0  ## Cr
    c = 0.0  ## Ci
    U = 0.0
    V = 0.0
    K = 1.5
    k = 1.0

    y = 0.
    while y < 150.:
        y += 1.

        x = 0.
        while x < 150.:
            x += 1.
            Z, z, T, t = 0.0, 0.0, 0.0, 0.0
            U = x * 2.
            U /= h
            V = y * 2.
            V /= h
            C = U - K
            c = V - k

            i = 0.
            while i < 50.:
                i += 1.
                if T + t <= 4.:
                    z = Z * z
                    z *= 2.
                    z += c
                    Z = T - t
                    Z += C
                    T = Z * Z
                    t = z * z

            if T + t <= 4.:
                count += 1

    return count



for i in range(0, ITERATIONS):
    result = mandelbrot()
    assert result == EXPECTED
