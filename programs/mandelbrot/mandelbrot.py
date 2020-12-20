EXPECTED = 8939


def mandelbrot() -> int:
    count: int = 0

    h: float = 150
    Z: float = 0.0  ## Zr
    z: float = 0.0  ## Zi
    T: float = 0.0  ## Tr
    t: float = 0.0  ## Ti
    C: float = 0.0  ## Cr
    c: float = 0.0  ## Ci
    U: float = 0.0
    V: float = 0.0
    K: float = 1.5
    k: float = 1.0

    y: float = 0
    while y < 150:
        y += 1

        x: float = 0
        while x < 150:
            x += 1
            Z, z, T, t = 0.0, 0.0, 0.0, 0.0
            U = x * 2
            U /= h
            V = y * 2
            V /= h
            C = U - K
            c = V - k

            i: float = 0
            while i < 50:
                i += 1
                if T + t <= 4:
                    z = Z * z
                    z *= 2
                    z += c
                    Z = T - t
                    Z += C
                    T = Z * Z
                    t = z * z

            if T + t <= 4:
                count += 1

    return count


for i in range(0, 10):
    result = mandelbrot()
    assert result == EXPECTED
