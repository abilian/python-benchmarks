ITERATIONS = 100
EXPECTED = 8939

try:
    import pyjion

    pyjion.enable()
except ImportError:
    pass

try:
    from numba import jit
except ImportError:
    jit = None


def mandelbrot() -> int:
    count: int = 0

    h: float = 150
    Z: float = 0.0  ## Zr
    z: float = 0.0  ## Zi
    T: float = 0.0  ## Tr
    t: float = 0.0  ## Ti
    C: float = 0.0  ## Cr
    c: float = 0.0  ## Ci
    K: float = 1.5
    k: float = 1.0

    y: float = 0
    while y < 150:
        y += 1

        x: float = 0
        while x < 150:
            x += 1
            Z, z, T, t = 0.0, 0.0, 0.0, 0.0

            C = (x * 2) / h - K
            c = (y * 2) / h- k

            i: float = 0
            while i < 50:
                i += 1
                if T + t <= 4:
                    z = (Z * z) * 2 + c
                    Z = T - t + C
                    T = Z * Z
                    t = z * z

            if T + t <= 4:
                count += 1

    return count


if jit:
    mandelbrot = jit(nopython=True, cache=True)(mandelbrot)


for i in range(0, ITERATIONS):
    result = mandelbrot()
    assert result == EXPECTED
