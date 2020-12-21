def mandelbrot() -> int:
    j = 0
    while j < 100:
        j = j + 1

        count = 0

        h = 150
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

        y = 0
        while y < 150:
            y = y + 1

            x = 0
            while x < 150:
                x = x + 1
                Z = 0.0
                z = 0.0
                T = 0.0
                t = 0.0
                U = x * 2
                U = U / h
                V = y * 2
                V = V / h
                C = U - K
                c = V - k

                i = 0
                while i < 50:
                    i = i + 1
                    if T + t <= 4:
                        z = Z * z
                        z = z * 2
                        z = z + c
                        Z = T - t
                        Z = Z + C
                        T = Z * Z
                        t = z * z

                if T + t <= 4:
                    count = count + 1

    return count
